def user_detail():
    name = input("\n\nHello, welcome to the cinema! Please may I kindly take your name? ")
    age = int(input(f"Thank you for that {name}! Please may I take your age aswell? "))
    movie = input(f"That is lovely {name}, now please may I take the name of the movie you wish to see? ")
    vip_status = input("Would you like a VIP ticket for an extra £20? ").lower()
    discount_code = input("Do you have a discount code? ")
    return name,age,movie,vip_status,discount_code

def get_ticket_price(age):
    if age > 17:
        return 10
    elif age >= 12:
        return 7
    else:
        return 5
    
def discountfunc(ticket_price, discount_code):
    if discount_code == "SAVE5":
        if ticket_price >= 5:
            Discount_Statement = "💸 Discount: £5"
            return 5, Discount_Statement
        else:
            Discount_Statement = "No Discount Applied. As the ticket price does not meet the threshold!"
            return 0, Discount_Statement
    else:
        Discount_Statement = "No Discount Applied"
        return 0, Discount_Statement
    
def vip_func(vip_status):
    if vip_status == "yes":
        vip_amount = 20
        vip_statement = "✨ VIP Ticket: £20"
    else:
        vip_amount = 0
        vip_statement = "Standard Ticket"
    return vip_amount, vip_statement

def print_ticket_summary(ticket, ticket_price, vip_statement, discount_statement):
    print(f"\n🎟️  Ticket for {ticket['name']} (Age: {ticket['age']})")
    print(f"🎬 Movie: {ticket['movie']}")
    print(f"💷 Your base price is £{ticket_price}")
    print(vip_statement)
    print(discount_statement)
    print(f"💷 Total Ticket Price: £{ticket['ticket_total']}\n")
    if ticket.get("snacks"):
        snack_lines = [f"  • {qty}x {snack} @ £{price:.2f} each"
            for snack, qty, price in ticket['snacks']]
        print("🍿 Snacks:")
        for line in snack_lines:
            print(line)
        print(f"   ➕ Snacks Total: £{ticket['snacks_total']:.2f}")
    else:
        print("🍿 Snacks: None")
    total = ticket.get('snacks_total', 0) + ticket['ticket_total']
    print(f"Total: £{total:.2f}\n")
    print("🍿 Enjoy the show!\n")
    return

def receipt_note(tickets, grand_total):
    with open("final_receipt.txt", "w") as file:
        file.write("--- Final Receipt ---\n")
        for ticket in tickets:
            name = ticket["name"]
            age = ticket["age"]
            movie = ticket["movie"]
            vip = ticket["vip_status"]
            vip_price = f"£{ticket['vip_price']:.2f}"
            discount = f"£{ticket['discount_amount']:.2f}"
            paid = f"£{ticket['ticket_total']:.2f}"
            
            if ticket.get('snacks'):
                snacks = ", ".join([f"{qty}x {snack}" for snack, qty, price in ticket['snacks']])
            else:
                snacks = "No snacks ordered"
            
            file.write(f"{name} (Age: {age}), Movie: {movie}, VIP: {vip}, VIP Price: {vip_price}, Discount: {discount}, Paid: {paid}, Snacks: {snacks}\n")
        
        file.write(f"\nWhole bill comes to £{grand_total:.2f}\n")

def ticket_system(tickets, purchasing):
    while purchasing.lower() == "yes":
        name,age,movie,vip_status,discount_code = user_detail()
        ticket_price = get_ticket_price(age)
        discount_amount, discount_statement = discountfunc(ticket_price, discount_code)
        vip_amount, vip_statement = vip_func(vip_status)
        ticket_total = (ticket_price + vip_amount) - discount_amount

        ticket = {
            "name": name,
            "age": age,
            "movie": movie,
            "vip_status": vip_status,
            "vip_price": vip_amount,
            "discount_amount": discount_amount,
            "ticket_total": ticket_total
        }
        tickets.append(ticket)
        

        if input(f"\nWould you like to purchase some snacks or juice {name}? ").lower() == "yes":
            snack_function(ticket)

        print_ticket_summary(ticket, ticket_price, vip_statement, discount_statement)
        
        purchasing = input(f"\nWould you like to purchase another ticket? ")

    print("\n--- Final Receipt ---")
    grand_total = 0

    for ticket in tickets:
        # Get ticket total
        ticket_total = ticket.get('ticket_total', 0)

        # Get snack total if it exists
        snacks_total = ticket.get('snacks_total', 0)

        # Add both to the running grand total
        grand_total += ticket_total + snacks_total

        # Format snack list
        if "snacks" in ticket and ticket["snacks"]:
            snack_list = ", ".join([f"{qty}x {snack}" for snack, qty, _ in ticket["snacks"]])
        else:
            snack_list = "None"

        # Show full receipt per person
        print(f"{ticket['name']} (Age: {ticket['age']}), Movie: {ticket['movie']}, "
            f"VIP: {ticket['vip_status']}, VIP Price: £{ticket['vip_price']:.2f}, "
            f"Discount: £{ticket['discount_amount']:.2f}, Paid: £{ticket_total:.2f}, "
            f"Snacks: {snack_list}, Snacks Total: £{snacks_total:.2f}")

    print(f"\n💷 Whole bill comes to £{grand_total:.2f}")

    receipt_note(tickets, grand_total)

    return

def ticket_main():
    tickets = []
    purchasing = "yes"
    ticket_system(tickets, purchasing)


    return

def snack_menu():
    snack_menu_items = {
    "popcorn": 3.50,
    "soda": 2.00,
    "nachos": 4.00,
    "candy": 1.50
    }

    print("\n🍿 Snack Menu:")
    for snack, price in snack_menu_items.items():
        print(f"{snack.title():<10} - £{price:.2f}")

    return snack_menu_items

def snack_ordering(ticket, snack_menu_items):
    all_snack_total_price = 0
    snack_order = []
    while True:
        snack_choice = input(f"\nPlease enter the snack you would like to purchase {ticket['name']}. (Type 'Done' when you have completed!) ").lower()
        if snack_choice == "done":
            break
        if snack_choice in snack_menu_items:
            try:
                quantity = int(input(f"How many {snack_choice} would you like? "))
                if quantity <= 0:
                    print("Please enter a positive quantity.")
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue
            snack_items_price = snack_menu_items[snack_choice] * quantity
            all_snack_total_price += snack_items_price
            snack_order.append((snack_choice, quantity, snack_items_price))
        else:
            print("❌ That snack isn't on the menu. Please choose again.")
    ticket["snacks"] = snack_order
    ticket["snacks_total"] = all_snack_total_price
    return

def snack_function(ticket):
    snack_menu_items = snack_menu()
    snack_ordering(ticket, snack_menu_items)
    return

ticket_main()