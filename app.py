
from flask import Flask, render_template, request,jsonify

from data import Restaurant, Food, SaleBook,show_menu

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



@app.route("/")

def index():
    title="Start Restaurant Menu"
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
if __name__=="__main__":
    app.run(port=3000,debug=True)