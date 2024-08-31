import argparse
def calculate_tip(bill_amount, tip_percentage):
    """
    Calculate the tip based on the bill amount and tip percentage.
    :param bill_amount: The total bill amount.
    :param tip_percentage: The percentage of the bill to be given as a tip.
    :return: The calculated tip amount.
    """
    try:
        tip_amount = bill_amount * (tip_percentage / 100)
        total_amount = bill_amount + tip_amount
        return tip_amount, total_amount
    except Exception as e:
        print(f"Error calculating tip: {e}")
        return None, None
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Tip Calculator: Calculate the tip and total payment for your bill. '
                                                 'Provide the bill amount and choose a tip percentage from the options '
                                                 'or input a custom percentage. The script will compute the tip and the total amount to be paid.')
    # Adding arguments for the script
    parser.add_argument('bill_amount', type=float, 
                        help='The total bill amount in dollars.')
    parser.add_argument('--tip', type=float, choices=[15, 18, 20],
                        help='The tip percentage to be applied. Choose from 15, 18, 20. For a custom percentage, use --custom-tip.')
    parser.add_argument('--custom-tip', type=float,
                        help='A custom tip percentage to be applied if the default choices are not suitable.')
    # Parse the arguments
    args = parser.parse_args()
    # Determine the tip percentage to use
    tip_percentage = args.tip if args.tip else args.custom_tip
    if tip_percentage is None:
        print("Please specify a tip percentage using --tip or --custom-tip.")
        return
    try:
        # Calculate the tip and total amount
        tip_amount, total_amount = calculate_tip(args.bill_amount, tip_percentage)
        if tip_amount is not None and total_amount is not None:
            # Display the results
            print(f"Bill Amount: ${args.bill_amount:.2f}")
            print(f"Tip Percentage: {tip_percentage}%")
            print(f"Tip Amount: ${tip_amount:.2f}")
            print(f"Total Amount to be Paid: ${total_amount:.2f}")
    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == '__main__':
    main()