from flask import Flask, request, jsonify

app = Flask(__name__)

# Constants
MAX_ACTIVE_NUMBERS = 100
MONEY_PER_UNIT = 5000

# Container for active numbers (money)
active_numbers = MAX_ACTIVE_NUMBERS

# Allowed bank accounts
allowed_accounts = ['1976278463', '20057942287']

@app.route('/get_active_numbers', methods=['GET'])
def get_active_numbers():
    return jsonify({'active_numbers': active_numbers}), 200

@app.route('/send_money', methods=['POST'])
def send_money():
    data = request.json
    bank_account = data.get('bank_account')

    if bank_account not in allowed_accounts:
        return jsonify({'error': 'Bank account not allowed'}), 403

    amount = data.get('amount')

    if amount is None or amount <= 0:
        return jsonify({'error': 'Invalid amount'}), 400

    global active_numbers
    units_to_send = amount // MONEY_PER_UNIT

    if units_to_send > active_numbers:
        return jsonify({'error': 'Not enough active numbers to send'}), 400

    active_numbers -= units_to_send

    return jsonify({'message': f'Successfully sent {amount} units to bank account {bank_account}'}), 200

if __name__ == '__main__':
    app.run(debug=True)
