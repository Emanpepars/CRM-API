from flask import Blueprint, request, jsonify
from models import db, Customer, Lead, Note, LEAD_STATUSES

api = Blueprint("api", __name__)


def error_response(message, status_code=400):
    return jsonify({"error": message}), status_code


def get_json_or_error():
    data = request.get_json(silent=True)
    if data is None:
        return None, error_response("Request body must be valid JSON", 400)
    return data, None


@api.route("/customers", methods=["GET"])
def list_customers():
    customers = Customer.query.all()
    return jsonify([c.to_dict() for c in customers])


@api.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return error_response("Customer not found", 404)
    return jsonify(customer.to_dict())


@api.route("/customers", methods=["POST"])
def create_customer():
    data, err = get_json_or_error()
    if err:
        return err

    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return error_response("Fields 'name' and 'email' are required")

    if Customer.query.filter_by(email=email).first():
        return error_response("A customer with this email already exists", 409)

    customer = Customer(
        name=name,
        email=email,
        phone=data.get("phone"),
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_dict()), 201


@api.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return error_response("Customer not found", 404)

    data, err = get_json_or_error()
    if err:
        return err

    if "name" in data:
        customer.name = data["name"]
    if "email" in data:
        customer.email = data["email"]
    if "phone" in data:
        customer.phone = data["phone"]

    db.session.commit()
    return jsonify(customer.to_dict())


@api.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return error_response("Customer not found", 404)

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted"})


@api.route("/leads", methods=["GET"])
def list_leads():
    query = Lead.query

    status = request.args.get("status")
    if status:
        if status not in LEAD_STATUSES:
            return error_response(
                f"Invalid status. Allowed: {', '.join(LEAD_STATUSES)}"
            )
        query = query.filter(Lead.status == status)

    search = request.args.get("search")
    if search:
        like = f"%{search}%"
        query = query.filter((Lead.name.ilike(like)) | (Lead.email.ilike(like)))

    leads = query.all()
    return jsonify([lead.to_dict() for lead in leads])


@api.route("/leads/<int:lead_id>", methods=["GET"])
def get_lead(lead_id):
    lead = Lead.query.get(lead_id)
    if not lead:
        return error_response("Lead not found", 404)
    return jsonify(lead.to_dict())


@api.route("/leads", methods=["POST"])
def create_lead():
    data, err = get_json_or_error()
    if err:
        return err

    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return error_response("Fields 'name' and 'email' are required")

    status = data.get("status", "new")
    if status not in LEAD_STATUSES:
        return error_response(
            f"Invalid status. Allowed: {', '.join(LEAD_STATUSES)}"
        )

    customer_id = data.get("customer_id")
    if customer_id is not None:
        if not Customer.query.get(customer_id):
            return error_response("Customer not found", 404)

    lead = Lead(
        name=name,
        email=email,
        phone=data.get("phone"),
        status=status,
        customer_id=customer_id,
    )
    db.session.add(lead)
    db.session.commit()
    return jsonify(lead.to_dict()), 201


@api.route("/leads/<int:lead_id>", methods=["PUT"])
def update_lead(lead_id):
    lead = Lead.query.get(lead_id)
    if not lead:
        return error_response("Lead not found", 404)

    data, err = get_json_or_error()
    if err:
        return err

    if "name" in data:
        lead.name = data["name"]
    if "email" in data:
        lead.email = data["email"]
    if "phone" in data:
        lead.phone = data["phone"]

    if "status" in data:
        if data["status"] not in LEAD_STATUSES:
            return error_response(
                f"Invalid status. Allowed: {', '.join(LEAD_STATUSES)}"
            )
        lead.status = data["status"]

    if "customer_id" in data:
        new_customer_id = data["customer_id"]
        if new_customer_id is not None and not Customer.query.get(new_customer_id):
            return error_response("Customer not found", 404)
        lead.customer_id = new_customer_id

    db.session.commit()
    return jsonify(lead.to_dict())


@api.route("/leads/<int:lead_id>", methods=["DELETE"])
def delete_lead(lead_id):
    lead = Lead.query.get(lead_id)
    if not lead:
        return error_response("Lead not found", 404)

    db.session.delete(lead)
    db.session.commit()
    return jsonify({"message": "Lead deleted"})


@api.route("/leads/<int:lead_id>/notes", methods=["GET"])
def list_notes_for_lead(lead_id):
    lead = Lead.query.get(lead_id)
    if not lead:
        return error_response("Lead not found", 404)
    return jsonify([note.to_dict() for note in lead.notes])


@api.route("/leads/<int:lead_id>/notes", methods=["POST"])
def create_note(lead_id):
    lead = Lead.query.get(lead_id)
    if not lead:
        return error_response("Lead not found", 404)

    data, err = get_json_or_error()
    if err:
        return err

    content = data.get("content")
    if not content:
        return error_response("Field 'content' is required")

    note = Note(content=content, lead_id=lead.id)
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_dict()), 201


@api.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return error_response("Note not found", 404)
    return jsonify(note.to_dict())


@api.route("/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return error_response("Note not found", 404)

    data, err = get_json_or_error()
    if err:
        return err

    if "content" in data:
        if not data["content"]:
            return error_response("Field 'content' cannot be empty")
        note.content = data["content"]

    db.session.commit()
    return jsonify(note.to_dict())


@api.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return error_response("Note not found", 404)

    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted"})


@api.route("/reports/leads", methods=["GET"])
def leads_report():
    total = Lead.query.count()
    won = Lead.query.filter_by(status="won").count()
    lost = Lead.query.filter_by(status="lost").count()

    conversion_rate = round((won / total) * 100, 2) if total > 0 else 0.0

    return jsonify({
        "total_leads": total,
        "won_leads": won,
        "lost_leads": lost,
        "conversion_rate": conversion_rate,
    })
