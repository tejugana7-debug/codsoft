import json
import os

class Contact:
    def __init__(self, name, phone, email, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["phone"], data["email"], data["address"])

class ContactManager:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.contacts = [Contact.from_dict(c) for c in data]
            except (json.JSONDecodeError, IOError):
                self.contacts = []
        else:
            self.contacts = []

    def save_contacts(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump([c.to_dict() for c in self.contacts], f, indent=4)
        except IOError as e:
            print(f"Error saving contacts: {e}")

    def add_contact(self, name, phone, email, address):
        new_contact = Contact(name, phone, email, address)
        self.contacts.append(new_contact)
        self.save_contacts()
        print("Contact added successfully.")

    def view_contacts(self):
        if not self.contacts:
            print("No contacts found.")
            return
        print("\n--- Contact List ---")
        for i, contact in enumerate(self.contacts, 1):
            print(f"{i}. Name: {contact.name}, Phone: {contact.phone}")

    def search_contact(self, keyword):
        results = [c for c in self.contacts if keyword.lower() in c.name.lower() or keyword in c.phone]
        if not results:
            print("No matching contacts found.")
        else:
            print("\n--- Search Results ---")
            for contact in results:
                print(f"Name: {contact.name}")
                print(f"Phone: {contact.phone}")
                print(f"Email: {contact.email}")
                print(f"Address: {contact.address}")
                print("-" * 20)

    def update_contact(self, name_to_update):
        for contact in self.contacts:
            if contact.name.lower() == name_to_update.lower():
                print(f"Updating contact: {contact.name}")
                contact.name = input(f"Enter new name ({contact.name}): ") or contact.name
                contact.phone = input(f"Enter new phone ({contact.phone}): ") or contact.phone
                contact.email = input(f"Enter new email ({contact.email}): ") or contact.email
                contact.address = input(f"Enter new address ({contact.address}): ") or contact.address
                self.save_contacts()
                print("Contact updated successfully.")
                return
        print("Contact not found.")

    def delete_contact(self, name_to_delete):
        for i, contact in enumerate(self.contacts):
            if contact.name.lower() == name_to_delete.lower():
                del self.contacts[i]
                self.save_contacts()
                print("Contact deleted successfully.")
                return
        print("Contact not found.")

def main():
    manager = ContactManager()

    while True:
        print("\n--- Contact Management System ---")
        print("1. Add Contact")
        print("2. View Contact List")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter Name: ")
            phone = input("Enter Phone Number: ")
            email = input("Enter Email: ")
            address = input("Enter Address: ")
            manager.add_contact(name, phone, email, address)
        elif choice == '2':
            manager.view_contacts()
        elif choice == '3':
            keyword = input("Enter Name or Phone Number to Search: ")
            manager.search_contact(keyword)
        elif choice == '4':
            name = input("Enter the Name of the contact to update: ")
            manager.update_contact(name)
        elif choice == '5':
            name = input("Enter the Name of the contact to delete: ")
            manager.delete_contact(name)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
