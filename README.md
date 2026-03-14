Overview

The Contacts Microservice allows users to save and manage trusted contacts that can be reused across features in a larger application. A user can add contacts, edit them, view only their own contact list, link contacts to specific items, view linked contacts for an item, remove an association, and retrieve contact details for context in another service.

This microservice stores data in a JSON file and was designed to be simple, readable, and easy to integrate into a larger Python project.

Features

This microservice supports the following actions:

Add a new contact

Edit an existing contact

View all contacts for a specific user

Associate a contact with an item

View contacts linked to an item

Remove a contact association from an item

Retrieve associated contact details for another service

View an audit log of association activity

Technologies Used

Python 3

JSON file storage

UUID for unique IDs

Regular expressions for input validation

datetime for timestamps

Project Structure
Contacts Microservice/
├── contacts_microservice.py
├── contacts_data.json
└── README.md

File Descriptions

contacts_microservice.py
Main microservice file containing the ContactsMicroservice class and all contact logic.

contacts_data.json
JSON storage file that keeps contact records, item associations, and audit log entries.

README.md
Documentation for the microservice.

How to Run / Use the Microservice

This microservice is not a Flask API. It is used by importing the Python class into another Python file.

Example
from contacts_microservice import ContactsMicroservice

service = ContactsMicroservice()

result = service.add_contact(
    user_id="user123",
    name="Alice Smith",
    email="alice@example.com",
    phone="301-555-1234"
)

print(result)


If contacts_data.json does not exist, the microservice automatically creates it.

Communication Contract

This microservice communicates through direct method calls in Python.
Another part of the program imports the class, creates an instance, and calls its methods.

Data Storage Format

The microservice stores data in contacts_data.json using this structure:

{
  "schema_version": "1.0",
  "contacts": [],
  "associations": [],
  "audit_log": []
}

Sections

contacts stores saved contact records

associations stores links between contacts and items

audit_log stores association history for traceability

Methods
1. Add Contact
add_contact(user_id, name, email="", phone="")


Adds a new contact for a user.

Parameters

user_id: owner of the contact

name: contact name

email: optional email

phone: optional phone number

Rules

name is required

at least one contact method is required: email or phone

email format must be valid if provided

phone format must be valid if provided

Example
service.add_contact(
    user_id="user123",
    name="Alice Smith",
    email="alice@example.com",
    phone="301-555-1234"
)

Example Response
{
  "status": "success",
  "message": "Contact added successfully.",
  "contact": {
    "contact_id": "generated-uuid",
    "user_id": "user123",
    "name": "Alice Smith",
    "email": "alice@example.com",
    "phone": "301-555-1234",
    "created_at": "2026-03-14T12:00:00Z",
    "updated_at": "2026-03-14T12:00:00Z"
  }
}

2. Edit Contact
edit_contact(user_id, contact_id, name=None, email=None, phone=None)


Updates an existing contact if it belongs to the given user.

Rules

only the owner can edit the contact

updated values must still pass validation

contact must exist

Example
service.edit_contact(
    user_id="user123",
    contact_id="contact-uuid",
    phone="240-555-9876"
)

3. List Contacts
list_contacts(user_id)


Returns only the contacts that belong to the specified user.

Example
service.list_contacts("user123")

Example Response
{
  "status": "success",
  "contacts": [
    {
      "contact_id": "generated-uuid",
      "user_id": "user123",
      "name": "Alice Smith",
      "email": "alice@example.com",
      "phone": "301-555-1234",
      "created_at": "2026-03-14T12:00:00Z",
      "updated_at": "2026-03-14T12:00:00Z"
    }
  ]
}

4. Associate Contact With Item
associate_contact_with_item(user_id, contact_id, item_type, item_id)


Links a saved contact to a specific item.

Valid item_type values

game

medication

task

Rules

contact must belong to the user

duplicate associations are prevented

successful associations are logged in the audit log

Example
service.associate_contact_with_item(
    user_id="user123",
    contact_id="contact-uuid",
    item_type="medication",
    item_id="med001"
)

5. Get Contacts for Item
get_contacts_for_item(user_id, item_type, item_id)


Returns all contacts linked to a specific item for that user.

Example
service.get_contacts_for_item(
    user_id="user123",
    item_type="medication",
    item_id="med001"
)

6. Get Contact Details for Context
get_contact_details_for_context(user_id, item_type, item_id)


Returns associated contact details in a structure that can be used by another service.

Example Use Cases

caregiver lookup

emergency contact lookup

task sharing

sending reminders to linked contacts

Example
service.get_contact_details_for_context(
    user_id="user123",
    item_type="medication",
    item_id="med001"
)

7. Remove Contact Association
remove_contact_association(user_id, contact_id, item_type, item_id)


Removes a link between a contact and an item.

Rules

association must exist

successful removals are logged in the audit log

Example
service.remove_contact_association(
    user_id="user123",
    contact_id="contact-uuid",
    item_type="medication",
    item_id="med001"
)

8. Get Audit Log
get_audit_log()


Returns the audit log entries for association creation and removal.

Example
service.get_audit_log()

Validation Rules

The microservice checks the following:

contact name cannot be empty

at least one contact method is required

email must match a valid format if provided

phone must match a valid format if provided

users can only edit and use their own contacts

duplicate item associations are not created

Example Data
Contact Record
{
  "contact_id": "uuid-value",
  "user_id": "user123",
  "name": "Alice Smith",
  "email": "alice@example.com",
  "phone": "301-555-1234",
  "created_at": "2026-03-14T12:00:00Z",
  "updated_at": "2026-03-14T12:00:00Z"
}

Association Record
{
  "association_id": "uuid-value",
  "user_id": "user123",
  "contact_id": "contact-uuid",
  "item_type": "medication",
  "item_id": "med001",
  "created_at": "2026-03-14T12:05:00Z"
}

Audit Log Record
{
  "action": "create_association",
  "user_id": "user123",
  "contact_id": "contact-uuid",
  "item_type": "medication",
  "item_id": "med001",
  "timestamp": "2026-03-14T12:05:00Z"
}

Quality Attributes
Security / Privacy

Users can only access and modify their own contacts and associations.

Validation

The microservice validates required fields and checks email/phone format before saving data.

Maintainability

The logic is organized into helper methods and clearly separated class methods, making the code easier to read and update.

Consistency

Data is stored in a consistent JSON structure with schema versioning.

Traceability

Association creation and removal are recorded in the audit log.
