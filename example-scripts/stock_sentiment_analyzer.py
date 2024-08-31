import argparse
from datetime import datetime, timedelta
import random
import json
import csv
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
import pandas as pd
def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="""
    Stock Sentiment Analyzer: Analyze stock market news headlines for sentiment and buzzword frequency.
    How to use:
    1. Specify news sources with --sources
    2. Set date range with --start-date and --end-date
    3. Define custom buzzwords with --buzzwords
    4. Choose output format with --output-format
    5. Set analysis frequency with --frequency
    Example:
    python stock_sentiment_analyzer.py --sources Bloomberg Reuters --start-date 2023-01-01 --end-date 2023-06-30 --buzzwords bullish bearish crypto --output-format csv --frequency weekly
    """)
    parser.add_argument('--sources', nargs='+', default=['Bloomberg', 'Reuters', 'CNBC'], help='List of news sources')
    parser.add_argument('--start-date', type=str, required=True, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, required=True, help='End date (YYYY-MM-DD)')
    parser.add_argument('--buzzwords', nargs='+', default=['bullish', 'bearish', 'volatility', 'recession', 'growth'], help='Custom buzzwords to track')
    parser.add_argument('--output-format', choices=['csv', 'json'], default='csv', help='Output format for data')
    parser.add_argument('--frequency', choices=['daily', 'weekly'], default='daily', help='Analysis frequency')
    return parser.parse_args()
def generate_dummy_headlines(start_date, end_date, sources, buzzwords):
    """Generate dummy headlines for the specified date range."""
    headlines = []
    current_date = start_date
    while current_date <= end_date:
        for _ in range(random.randint(1, 5)):  # 1-5 headlines per day
            source = random.choice(sources)
            headline = f"{random.choice(['Stock market', 'Dow', 'S&P 500', 'NASDAQ'])} "
            headline += f"{random.choice(['rises', 'falls', 'remains stable'])} "
            headline += f"as {random.choice(['investors', 'traders', 'analysts'])} "
            headline += f"{random.choice(['react to', 'consider', 'weigh'])}"
            # Add a buzzword with 30% probability
            if random.random() < 0.3:
                headline += f" {random.choice(buzzwords)}"
            headlines.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'source': source,
                'headline': headline
            })
        current_date += timedelta(days=1)
    return headlines
def analyze_sentiment(headline):
    """Analyze sentiment of a headline using TextBlob."""
    return TextBlob(headline).sentiment.polarity
def count_buzzwords(headline, buzzwords):
    """Count occurrences of buzzwords in a headline."""
    return sum(buzzword.lower() in headline.lower() for buzzword in buzzwords)
def aggregate_data(headlines, buzzwords, frequency):
    """Aggregate headline data based on the specified frequency."""
    df = pd.DataFrame(headlines)
    df['date'] = pd.to_datetime(df['date'])
    df['sentiment'] = df['headline'].apply(analyze_sentiment)
    df['buzzword_count'] = df['headline'].apply(lambda x: count_buzzwords(x, buzzwords))
    if frequency == 'weekly':
        df['date'] = df['date'].dt.to_period('W').apply(lambda r: r.start_time)
    aggregated = df.groupby('date').agg({
        'sentiment': 'mean',
        'buzzword_count': 'sum'
    }).reset_index()
    return aggregated
def visualize_data(data):
    """Create visualizations for sentiment and buzzword frequency."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    sns.lineplot(x='date', y='sentiment', data=data, ax=ax1)
    ax1.set_title('Sentiment Trend Over Time')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Average Sentiment')
    sns.barplot(x='date', y='buzzword_count', data=data, ax=ax2)
    ax2.set_title('Buzzword Frequency Over Time')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Buzzword Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('stock_sentiment_analysis.png')
    print("Visualization saved as 'stock_sentiment_analysis.png'")
def save_data(data, output_format):
    """Save aggregated data to a file in the specified format."""
    filename = f'stock_sentiment_data.{output_format}'
    if output_format == 'csv':
        data.to_csv(filename, index=False)
    elif output_format == 'json':
        data.to_json(filename, orient='records', date_format='iso')
    print(f"Data saved as '{filename}'")
def main():
    args = parse_arguments()
    try:
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD.")
        return
    if start_date > end_date:
        print("Error: Start date must be before end date.")
        return
    print("Generating dummy headlines...")
    headlines = generate_dummy_headlines(start_date, end_date, args.sources, args.buzzwords)
    print("Analyzing sentiment and counting buzzwords...")
    aggregated_data = aggregate_data(headlines, args.buzzwords, args.frequency)
    print("Creating visualizations...")
    visualize_data(aggregated_data)
    print(f"Saving data in {args.output_format} format...")
    save_data(aggregated_data, args.output_format)
    print("Analysis complete!")
if __name__ == "__main__":
    main()