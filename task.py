from flask import Flask, request, render_template, jsonify
import math

app = Flask(__name__)

@app.route('/')
def transaction_form():
    return render_template('form.html')

@app.route('/process_transaction', methods=['POST'])
def process_transaction():
    try:
        # Get data from the form
        userId = request.form['userId']
        listingId = request.form['listingId']
        recipient = request.form['recipient']
        price = request.form['price']
        timestamp = request.form['timestamp']
        currency = request.form['currency']

        # Validate data
        if not isinstance(userId, str) or not userId:
            return jsonify({"error": "User ID must be a non-empty string"}), 400

        if not isinstance(listingId, str) or not listingId:
            return jsonify({"error": "Listing ID must be a non-empty string"}), 400

        if not isinstance(recipient, str) or not recipient:
            return jsonify({"error": "Recipient must be a non-empty string"}), 400

        try:
            price = float(price)
            if price <= 0:
                raise ValueError()
        except ValueError:
            return jsonify({"error": "Price must be greater than 0"}), 400

        try:
            timestamp = int(timestamp)
        except ValueError:
            return jsonify({"error": "Timestamp must be an integer"}), 400

        if currency not in ["usd", "eur"]:
            return jsonify({"error": "Currency must be 'usd' or 'eur'"}), 400

        # Pricing calculation
        local_fee = 0.03 if currency == "usd" else 0.04
        final_price = price * (1 + local_fee)

        # Round up to two decimal places
        final_price = math.ceil(final_price * 100) / 100

        # Ensure final price meets the minimum values
        if currency == "usd" and final_price < 3:
            final_price = 3
        elif currency == "eur" and final_price < 2.8:
            final_price = 2.8

        # Update timestamp (increment by 1)
        timestamp += 1

        # Return the transaction response
        response = {
            "Final price": final_price,
            "Timestamp": timestamp
        }
        return jsonify(response)

    #Return Error
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
