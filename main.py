import json

# TODO: dodati typehinting na sve funkcije!
from typing import List, Union, Any

OFFERS_FILE = "offers.json"
PRODUCTS_FILE = "products.json"
CUSTOMERS_FILE = "customers.json"


def load_data(filename):
    """Load data from a JSON file."""
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Error decoding {filename}. Check file format.")
        return []


def save_data(filename, data):
    """Save data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# TODO: Implementirajte funkciju za kreiranje nove ponude.
def create_new_offer(offers: List[dict[str, Any]], products: List[dict[str, Any]], customers: List[dict[str, Any]]) -> None:
    """
    Prompt user to create a new offer by selecting a customer, entering date,
    choosing products, and calculating totals.
    """
    # Omogućite unos kupca
    # Izračunajte sub_total, tax i total
    # Dodajte novu ponudu u listu offers
    # Display customers and prompt for selection
    print("\nDostupni kupci:")
    for i, customer in enumerate(customers, start=1):
        print(f"{i}. {customer['name']} (Email: {customer['email']})")
    
    try:
        customer_index = int(input("Unesite broj za odabir kupca: ")) - 1
        if customer_index < 0 or customer_index >= len(customers):
            print("Neispravan izbor. Molimo pokušajte ponovno.")
            return
    except ValueError:
        print("Neispravan unos. Molimo unesite broj.")
        return
    
    selected_customer = customers[customer_index]

    # Prompt for date input
    from datetime import datetime
    date_input = input("Unesite datum ponude (YYYY-MM-DD): ").strip()
    try:
        date = datetime.strptime(date_input, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        print("Neispravan format datuma. Molimo koristite format YYYY-MM-DD.")
        return

    # Display products and prompt for selection and quantities
    items: List[dict[str, Union[str, int, float]]] = []
    print("\nDostupni proizvodi:")
    for i, product in enumerate(products, start=1):
        print(f"{i}. {product['name']} - ${product['price']:.2f} (ID: {product['id']})")
    
    while True:
        try:
            product_index = int(input("Unesite broj za odabir proizvoda (ili 0 za kraj): ")) - 1
            if product_index == -1:
                break
            if product_index < 0 or product_index >= len(products):
                print("Neispravan izbor proizvoda.")
                continue
            
            selected_product = products[product_index]
            quantity = int(input(f"Unesite kolicinu za '{selected_product['name']}': "))
            if quantity <= 0:
                print("Kolicina mora biti pozitivan broj.")
                continue

            item_total = selected_product['price'] * quantity
            items.append({
                "product_id": selected_product['id'],
                "product_name": selected_product['name'],
                "description": selected_product['description'],
                "price": selected_product['price'],
                "quantity": quantity,
                "item_total": item_total
            })

        except ValueError:
            print("Neispravan unos. Molimo unesite broj.")
    
    if not items:
        print("Ponuda mora imati barem jedan proizvod.")
        return

    # Calculate totals
    sub_total: float = sum(item['item_total'] for item in items)
    tax: float = sub_total * 0.1  # Assume a 10% tax rate
    total: float = sub_total + tax

    # Create a new offer
    new_offer_number: int = max((offer['offer_number'] for offer in offers), default=0) + 1
    new_offer: dict[str, Any] = {
        "offer_number": new_offer_number,
        "customer": selected_customer['name'],
        "date": date,
        "items": items,
        "sub_total": sub_total,
        "tax": tax,
        "total": total
    }

    # Append the new offer to the offers list
    offers.append(new_offer)

    # Spremanje novih podataka u JSON file
    save_data(OFFERS_FILE, offers)
    
    print("\nNova ponuda je uspješno kreirana!")
    print_offer(new_offer)


# TODO: Implementirajte funkciju za upravljanje proizvodima.
def manage_products(products: List[dict]) -> None:
    """
    Allows the user to add a new product or modify an existing product.
    """
    # Omogućite korisniku izbor između dodavanja ili izmjene proizvoda
    # Za dodavanje: unesite podatke o proizvodu i dodajte ga u listu products
    # Za izmjenu: selektirajte proizvod i ažurirajte podatke
    print("\nUpravljanje proizvodima")
    print("1. Dodaj novi proivod")
    print("2. Izmjeni postojeci proizvod")
    
    choice = input("Unesi izbor (1 or 2): ")
    
    # Dodavanje novog proizvoda
    if choice == '1':
        new_id = max(product['id'] for product in products) + 1 if products else 1
        name = input("Unesi ime proizvoda: ")
        description = input("Unesi opis proizvoda: ")
        try:
            price = float(input("Unesi cijenu proizvoda: "))
        except ValueError:
            print("Kriva cijena. Molim unesite ispavan broj.")
            return

        new_product = {
            "id": new_id,
            "name": name,
            "description": description,
            "price": price
        }
        
        products.append(new_product)
        print("Novi proizvod uspjesno dodan!")
        
        # Spremanje novih podataka u JSON file
        save_data(PRODUCTS_FILE, products)

    # Izmjena postojeceg proizvoda
    elif choice == '2':
        print("Izaberi proizvod za izmjenu:")
        for i, product in enumerate(products, start=1):
            print(f"{i}. {product['name']} - ${product['price']:.2f}")

        try:
            product_index = int(input("Unesi broj proizvoda: ")) - 1
            if product_index < 0 or product_index >= len(products):
                print("Neispravan proizvod.")
                return
        except ValueError:
            print("Neispravan unos. Molim unesite broj proizvoda.")
            return

        selected_product = products[product_index]
        
        new_name = input(f"Unesi novo ime (pritisni Enter da zadrzis '{selected_product['name']}'): ")
        new_description = input(f"Unesi novi opis (pritisni Enter da zadrzis ): {selected_product['description']}'): ")
        new_price_input = input(f"Enter new price (press Enter to keep ${selected_product['price']:.2f}): ")

        if new_name:
            selected_product['name'] = new_name
        if new_description:
            selected_product['description'] = new_description
        if new_price_input:
            try:
                selected_product['price'] = float(new_price_input)
            except ValueError:
                print("Neispravan unos cijene. Cijena nije promjenjena.")

        print("Proizvod izmjenjen uspjesno4!")
        
        # Spremanje novih podataka u JSON file
        save_data(PRODUCTS_FILE, products)

    else:
        print("Neispravan izbor. Molim odaberite 1 ili 2")


# TODO: Implementirajte funkciju za upravljanje kupcima.
def manage_customers(customers: List[dict]) -> None:
    """
    Allows the user to add a new customer or view all customers.
    """
    # Za dodavanje: omogući unos imena kupca, emaila i unos VAT ID-a
    # Za pregled: prikaži listu svih kupaca

    print("\nUpravljanje kupcima")
    print("1. Dodaj novog kupca")
    print("2. Vidi sve kupce")
    
    choice = input("Unesite svoj izbor (1 or 2): ")
    
    # Dodavanje novog kupca
    if choice == '1':
        name = input("Unesi ime kupca: ").strip()
        email = input("Unesi email kupca: ").strip()
        vat_id = input("Unesi VAT ID: ").strip()
        
        if not name or not email or not vat_id:
            print("Sva polja su obavezna.")
            return
        
        
        new_customer = {
            "name": name,
            "email": email,
            "vat_id": vat_id
        }
        
        customers.append(new_customer)
        print("Novi kupac dodan uspjesno!")
        
        # Spremanje novih podataka u JSON file
        save_data(CUSTOMERS_FILE, customers)
    
    # Lista svih kupaca
    elif choice == '2':
        if not customers:
            print("Nije pronaden kupac.")
        else:
            print("\nLista kupaca:")
            for i, customer in enumerate(customers, start=1):
                print(f"{i}. Name: {customer['name']}, Email: {customer['email']}, VAT ID: {customer['vat_id']}")
    else:
        print("Neispravan izbor. Molim odaberite 1 ili 2.")



# TODO: Implementirajte funkciju za prikaz ponuda.
def display_offers(offers: List[dict[str, Any]]) -> None:
    """
    Display all offers, offers for a selected month, or a single offer by ID.
    """
    # Omogućite izbor pregleda: sve ponude, po mjesecu ili pojedinačna ponuda
    # Prikaz relevantnih ponuda na temelju izbora
    print("\nIzbor pregleda ponuda:")
    print("1. Vidi sve ponude")
    print("2. Vidi ponude po mjesecu")
    print("3. Vidi detalje ponude po ID-u")

    choice = input("Unesi izbor (1-3): ").strip()

    if choice == "1":
        print("\nPrikaz svih ponuda:")
        for offer in offers:
            print_offer_summary(offer)

    elif choice == "2":
        month = input("\nUnesi Mjesec (YYYY-MM): ").strip()
        try:
            # Validate input date format
            from datetime import datetime
            datetime.strptime(month, "%Y-%m")
            filtered_offers = [
                offer for offer in offers if offer["date"].startswith(month)
            ]
            if filtered_offers:
                print(f"\nPonude za {month}:")
                for offer in filtered_offers:
                    print_offer_summary(offer)
            else:
                print(f"Nema ponuda za {month}.")
        except ValueError:
            print("Neispravan fromat datuma. Molim koristiti YYYY-MM.")

    elif choice == "3":
        try:
            offer_id = int(input("\nUnesi ID ponude: ").strip())
            offer = next(
                (o for o in offers if o["offer_number"] == offer_id), None
            )
            if offer:
                print("\nPrikaz detalja ponude:")
                print_offer(offer)
            else:
                print(f"Nije pronadena ponuda po ID-u {offer_id}.")
        except ValueError:
            print("Nevaljan ID. Unesite broj.")

    else:
        print("Neispravan izbor. Unesite validnu opciju (1-3).")


def print_offer_summary(offer: dict[str, Any]) -> None:
    """Display summary of multiple offers"""
    print(f"Offer #{offer['offer_number']} | Customer: {offer['customer']} | Date: {offer['date']} | Ukupno: ${offer['sub_total']} | Porez: ${offer['tax']} | Total: ${offer['total']:.2f}")



# Pomoćna funkcija za prikaz jedne ponude
def print_offer(offer: dict[str, Any]) -> None:
    """Display details of a single offer."""
    print(f"Ponuda br: {offer['offer_number']}, Kupac: {offer['customer']['name']}, Datum ponude: {offer['date']}")
    print("Stavke:")
    for item in offer["items"]:
        print(f"  - {item['product_name']} (ID: {item['product_id']}): {item['description']}")
        print(f"    Kolicina: {item['quantity']}, Cijena: ${item['price']}, Ukupno: ${item['item_total']}")
    print(f"Ukupno: ${offer['sub_total']}, Porez: ${offer['tax']}, Ukupno za platiti: ${offer['total']}")


def main():
    # Učitavanje podataka iz JSON datoteka
    offers = load_data(OFFERS_FILE)
    products = load_data(PRODUCTS_FILE)
    customers = load_data(CUSTOMERS_FILE)

    while True:
        print("\nOffers Calculator izbornik:")
        print("1. Kreiraj novu ponudu")
        print("2. Upravljanje proizvodima")
        print("3. Upravljanje korisnicima")
        print("4. Prikaz ponuda")
        print("5. Izlaz")
        choice = input("Odabrana opcija: ")

        if choice == "1":
            create_new_offer(offers, products, customers)
        elif choice == "2":
            manage_products(products)
        elif choice == "3":
            manage_customers(customers)
        elif choice == "4":
            display_offers(offers)
        elif choice == "5":
            # Pohrana podataka prilikom izlaza
            save_data(OFFERS_FILE, offers)
            save_data(PRODUCTS_FILE, products)
            save_data(CUSTOMERS_FILE, customers)
            break
        else:
            print("Krivi izbor. Pokusajte ponovno.")


if __name__ == "__main__":
    main()
