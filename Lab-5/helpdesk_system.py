"""A simple IT helpdesk ticket management system."""

import json
import os
from datetime import datetime

TICKETS = {}
TICKET_COUNTER = 100
ADMIN_PASSWORD = os.getenv("HELPDESK_ADMIN_PASSWORD")


def raise_ticket(user, issue_type, urgency="3", audit_trail=None):
    """Create a ticket and record its creation in the audit trail."""
    global TICKET_COUNTER

    priority = int(urgency)
    if not 1 <= priority <= 5:
        raise ValueError("Urgency must be between 1 and 5.")

    TICKET_COUNTER += 1
    TICKETS[TICKET_COUNTER] = {
        "user": user,
        "issue": issue_type,
        "priority": priority,
        "tech": None,
        "notes": [],
    }

    if audit_trail is None:
        audit_trail = []
    audit_trail.append(
        f"{user} raised #{TICKET_COUNTER} at {datetime.now()}"
    )
    return TICKET_COUNTER


def assign_ticket(ticket_id, technician):
    """Assign an existing ticket to a technician."""
    if ticket_id not in TICKETS:
        raise KeyError(f"Ticket {ticket_id} does not exist.")
    TICKETS[ticket_id]["tech"] = technician


def add_note(ticket_id, note):
    """Add a note to an existing ticket."""
    if ticket_id not in TICKETS:
        raise KeyError(f"Ticket {ticket_id} does not exist.")
    TICKETS[ticket_id]["notes"].append(note)


def close_ticket(ticket_id, password):
    """Close a ticket if the configured administrator password matches."""
    if not ADMIN_PASSWORD:
        raise RuntimeError(
            "Set the HELPDESK_ADMIN_PASSWORD environment variable first."
        )
    if password != ADMIN_PASSWORD:
        raise PermissionError("Invalid administrator password.")
    if ticket_id not in TICKETS:
        raise KeyError(f"Ticket {ticket_id} does not exist.")
    del TICKETS[ticket_id]


def unresolved_high_priority():
    """Return unassigned tickets with priority 4 or 5."""
    return [
        ticket_id
        for ticket_id, ticket in TICKETS.items()
        if ticket["priority"] >= 4 and ticket["tech"] is None
    ]


def save_tickets(file="tickets.json"):
    """Save current tickets as JSON."""
    with open(file, "w", encoding="utf-8") as ticket_file:
        json.dump(TICKETS, ticket_file, indent=2)


def main():
    """Demonstrate basic ticket management operations."""
    ticket_one = raise_ticket("anil", "printer", "5")
    raise_ticket("meera", "wifi", "4")
    ticket_three = raise_ticket("joe", "vpn", "3")

    assign_ticket(ticket_one, "Tech-Kiran")
    add_note(ticket_one, "Called user")
    print("Unassigned high priority:", unresolved_high_priority())

    level = input(
        "Urgency for a new laptop ticket (1-5, Enter for 3): "
    ).strip() or "3"

    try:
        raise_ticket("sana", "laptop", level)
    except ValueError:
        print("Invalid urgency. Enter a number from 1 to 5.")
        return

    if ADMIN_PASSWORD:
        close_ticket(ticket_three, ADMIN_PASSWORD)
    else:
        print("Ticket not closed: administrator password is not configured.")

    save_tickets()
    print("Open tickets:", list(TICKETS.keys()))


if __name__ == "__main__":
    main()
