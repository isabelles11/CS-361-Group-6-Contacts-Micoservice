import json
import os
import re
import uuid
from datetime import datetime


class ContactsMicroservice:
    """
    Contacts Microservice
    ---------------------
    This microservice lets users:
    1. Add contacts
    2. Edit contacts
    3. View only their own contacts
    4. Link contacts to items (game, med, or task)
    5. View linked contacts for an item
    6. Remove a contact association
    7. Retrieve contact details for another service to use

    Data is stored in a JSON file for simplicity.
    """

    SCHEMA_VERSION = "1.0"

    def __init__(self, data_file="contacts_data.json"):
        self.data_file = data_file
        self._load_data()

    def _load_data(self):
        """Load existing JSON data, or create a fresh structure if file doesn't exist."""
        if not os.path.exists(self.data_file):
            self.data = {
                "schema_version": self.SCHEMA_VERSION,
                "contacts": [],
                "associations": [],
                "audit_log": []
            }
            self._save_data()
        else:
            with open(self.data_file, "r", encoding="utf-8") as file:
                self.data = json.load(file)

    def _save_data(self):
        """Save current data back to JSON file."""
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)

    def _timestamp(self):
        """Return current UTC timestamp as a readable string."""
        return datetime.utcnow().isoformat() + "Z"

    def _is_valid_email(self, email):
        """Basic email validation."""
        if email is None or email == "":
            return True
        pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        return re.match(pattern, email) is not None

    def _is_valid_phone(self, phone):
        """Basic phone validation for simple formats."""
        if phone is None or phone == "":
            return True
        pattern = r"^\+?[0-9\s\-\(\)]{7,20}$"
        return re.match(pattern, phone) is not None

    def _validate_contact_input(self, name, email, phone):
        """Check contact fields and return error message if invalid."""
        if not name or not name.strip():
            return {"status": "error", "message": "Contact name is required."}

        if (not email or email.strip() == "") and (not phone or phone.strip() == ""):
            return {
                "status": "error",
                "message": "At least one contact method (email or phone) is required."
            }

        if email and not self._is_valid_email(email):
            return {"status": "error", "message": "Invalid email format."}

        if phone and not self._is_valid_phone(phone):
            return {"status": "error", "message": "Invalid phone format."}

        return None

    def add_contact(self, user_id, name, email="", phone=""):
        """
        Add a new contact for a specific user.
        Creates a unique contact_id.
        """
        validation_error = self._validate_contact_input(name, email, phone)
        if validation_error:
            return validation_error

        new_contact = {
            "contact_id": str(uuid.uuid4()),
            "user_id": user_id,
            "name": name.strip(),
            "email": email.strip() if email else "",
            "phone": phone.strip() if phone else "",
            "created_at": self._timestamp(),
            "updated_at": self._timestamp()
        }

        self.data["contacts"].append(new_contact)
        self._save_data()

        return {
            "status": "success",
            "message": "Contact added successfully.",
            "contact": new_contact
        }

    def edit_contact(self, user_id, contact_id, name=None, email=None, phone=None):
        """
        Edit an existing contact.
        Only the owner can edit their contact.
        """
        for contact in self.data["contacts"]:
            if contact["contact_id"] == contact_id and contact["user_id"] == user_id:
                new_name = name if name is not None else contact["name"]
                new_email = email if email is not None else contact["email"]
                new_phone = phone if phone is not None else contact["phone"]

                validation_error = self._validate_contact_input(new_name, new_email, new_phone)
                if validation_error:
                    return validation_error

                contact["name"] = new_name.strip()
                contact["email"] = new_email.strip() if new_email else ""
                contact["phone"] = new_phone.strip() if new_phone else ""
                contact["updated_at"] = self._timestamp()

                self._save_data()

                return {
                    "status": "success",
                    "message": "Contact updated successfully.",
                    "contact": contact
                }

        return {
            "status": "error",
            "message": "Contact not found or access denied."
        }

    def list_contacts(self, user_id):
        """
        Return only contacts that belong to the given user.
        """
        user_contacts = [
            contact for contact in self.data["contacts"]
            if contact["user_id"] == user_id
        ]

        return {
            "status": "success",
            "contacts": user_contacts
        }

    def associate_contact_with_item(self, user_id, contact_id, item_type, item_id):
        """
        Link a saved contact to an item like a game, medication, or task.
        Prevent duplicate links.
        """
        valid_item_types = {"game", "medication", "task"}
        if item_type not in valid_item_types:
            return {
                "status": "error",
                "message": "Invalid item_type. Must be game, medication, or task."
            }

        # Make sure the contact belongs to the user
        contact_exists = any(
            contact["contact_id"] == contact_id and contact["user_id"] == user_id
            for contact in self.data["contacts"]
        )

        if not contact_exists:
            return {
                "status": "error",
                "message": "Contact not found or access denied."
            }

        # Check for duplicate association
        for association in self.data["associations"]:
            if (
                association["user_id"] == user_id and
                association["contact_id"] == contact_id and
                association["item_type"] == item_type and
                association["item_id"] == item_id
            ):
                return {
                    "status": "success",
                    "message": "Association already exists.",
                    "association": association
                }

        new_association = {
            "association_id": str(uuid.uuid4()),
            "user_id": user_id,
            "contact_id": contact_id,
            "item_type": item_type,
            "item_id": item_id,
            "created_at": self._timestamp()
        }

        self.data["associations"].append(new_association)

        self.data["audit_log"].append({
            "action": "create_association",
            "user_id": user_id,
            "contact_id": contact_id,
            "item_type": item_type,
            "item_id": item_id,
            "timestamp": self._timestamp()
        })

        self._save_data()

        return {
            "status": "success",
            "message": "Contact associated with item successfully.",
            "association": new_association
        }

    def get_contacts_for_item(self, user_id, item_type, item_id):
        """
        Get all contacts linked to a specific item for the logged-in user.
        """
        linked_contact_ids = [
            assoc["contact_id"]
            for assoc in self.data["associations"]
            if assoc["user_id"] == user_id
            and assoc["item_type"] == item_type
            and assoc["item_id"] == item_id
        ]

        linked_contacts = [
            contact for contact in self.data["contacts"]
            if contact["user_id"] == user_id and contact["contact_id"] in linked_contact_ids
        ]

        return {
            "status": "success",
            "item_type": item_type,
            "item_id": item_id,
            "contacts": linked_contacts
        }

    def get_contact_details_for_context(self, user_id, item_type, item_id):
        """
        Returns associated contact details for another service to use.
        Example use cases:
        - caregiver lookup
        - meeting attendee info
        - task sharing
        """
        result = self.get_contacts_for_item(user_id, item_type, item_id)

        return {
            "status": "success",
            "message": "Associated contact details retrieved successfully.",
            "context": {
                "user_id": user_id,
                "item_type": item_type,
                "item_id": item_id
            },
            "contacts": result["contacts"]
        }

    def remove_contact_association(self, user_id, contact_id, item_type, item_id):
        """
        Remove a contact link from an item.
        """
        for i, association in enumerate(self.data["associations"]):
            if (
                association["user_id"] == user_id and
                association["contact_id"] == contact_id and
                association["item_type"] == item_type and
                association["item_id"] == item_id
            ):
                removed = self.data["associations"].pop(i)

                self.data["audit_log"].append({
                    "action": "remove_association",
                    "user_id": user_id,
                    "contact_id": contact_id,
                    "item_type": item_type,
                    "item_id": item_id,
                    "timestamp": self._timestamp()
                })

                self._save_data()

                return {
                    "status": "success",
                    "message": "Association removed successfully.",
                    "association": removed
                }

        return {
            "status": "error",
            "message": "Association not found or access denied."
        }

    def get_audit_log(self):
        """
        Returns audit log entries.
        Useful for traceability.
        """
        return {
            "status": "success",
            "audit_log": self.data["audit_log"]
        }
