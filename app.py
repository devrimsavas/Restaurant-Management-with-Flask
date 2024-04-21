
from flask import Flask, render_template, request,jsonify,Response

from data import Restaurant, Food, SaleBook,show_menu
from datetime import date, datetime
import json

app = Flask(__name__,template_folder='templates')


# Define your_first_menu function
def your_first_menu(restaurant):
    # Create the food items
    burger = Food('Burger', 10)
    pizza = Food('Pizza', 12)
    fried_chicken = Food('Fried Chicken', 9)
    spaghetti = Food('Spaghetti', 11)
    salad = Food('Salad', 8)
    lasagna = Food('Lasagna', 15)
    sushi = Food('Sushi', 20)
    tacho = Food('Tacho', 19)

    # Add the food items to the menu
    restaurant.add_an_food_to_menu(burger)
    restaurant.add_an_food_to_menu(pizza)
    restaurant.add_an_food_to_menu(fried_chicken)
    restaurant.add_an_food_to_menu(spaghetti)
    restaurant.add_an_food_to_menu(salad)
    restaurant.add_an_food_to_menu(lasagna)
    restaurant.add_an_food_to_menu(sushi)
    restaurant.add_an_food_to_menu(tacho)

# Initialize your restaurant and menu
your_restaurant = Restaurant('STAR RESTAURANT')
your_first_menu(your_restaurant)
customers=[]



@app.route("/")

def index():
    title="Star Restaurant Menu"
    data= {"title":title}
    menu_data=your_restaurant.display_menu()
    #return jsonify(data)
    return render_template('index.html',title=title,menu=menu_data)


@app.route("/menu")
def menu():
    menu_data=your_restaurant.display_menu()
    #return jsonify(menu_data)
    return render_template('index.html',menu=menu_data)

@app.route("/addnewfood",methods=["POST"])
def addnewfood():
    new_food_name=request.form.get("newfoodname")
    new_food_price=float(request.form.get("newfoodprice"))
    your_restaurant.add_an_food_to_menu(Food(new_food_name,new_food_price))
    return render_template('index.html')


@app.route("/updatefoodprice", methods=["POST"])
def updatefoodprice():
    update_food_name = request.form.get("updatefoodname")
    update_food_price = float(request.form.get("updatefoodprice"))

    # Find the food item in the restaurant's menu and update its price
    for food_item in your_restaurant.menu:
        if food_item.food_name == update_food_name:
            message = food_item.update_food_price(update_food_price)
            break
    else:
        message = f"Food item '{update_food_name}' not found in the menu"

    # Render the template with the message
    return render_template('index.html', message=message)

@app.route("/removefood", methods=["POST"])
def removefood():
    remove_food_name = request.form.get("removefoodname")
    your_restaurant.remove_food_from_menu(remove_food_name)
    return render_template('index.html')


@app.route("/about",methods=["GET"]) 
def about():
    return render_template('about.html')



def initialize_orders_file():
    try:
        with open("orders.json", "r") as file:
            # Try to parse the JSON file
            json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file does not exist or is empty/corrupted, initialize it
        with open("orders.json", "w") as file:
            json.dump({}, file)  # Write an empty dictionary

@app.route('/getorder', methods=["POST"])
def getorder():
    customer = request.form.get("customername")
    order_name = request.form.get("getordername")
    quantity = int(request.form.get("getorderquantity"))

    # Calculate the total price
    total_price = 0
    menu_item = next((item for item in your_restaurant.menu if item.food_name == order_name), None)
    if menu_item:
        total_price = menu_item.food_price * quantity

    # Current timestamp
    current_time = datetime.now().isoformat()
    
    # Load existing data
    with open("orders.json", "r") as file:
        orders = json.load(file)

    # Append new order to customer's list of orders
    if customer not in orders:
        orders[customer] = {"orders": [], "total_paid": 0}
    
    orders[customer]["orders"].append({
        "item": order_name,
        "quantity": quantity,
        "total_price": total_price,
        "timestamp": current_time
    })
    orders[customer]["total_paid"] += total_price

    # Save updated data
    with open("orders.json", "w") as file:
        json.dump(orders, file, indent=4)

    # Generate receipt text
    receipt_text = f"<h1>Receipt for {customer}</h1>"
    receipt_text += "<ul>"
    for order in orders[customer]["orders"]:
        receipt_text += f"<li>{order['quantity']}x {order['item']} at ${order['total_price']:.2f} each</li>"
    receipt_text += "</ul>"
    receipt_text += f"<strong>Total Paid: ${orders[customer]['total_paid']:.2f}</strong>"

    return jsonify({
        "customer_data": orders[customer],
        "receipt_text": receipt_text
    })



if __name__=="__main__":
    initialize_orders_file()
    app.run(host='0.0.0.0',port=3000,debug=True)