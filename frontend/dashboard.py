import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"  # Update if needed

def fetch_coins():
    # requests.get(f"{BASE_URL}/refresh-dashboard")
    res = requests.get(f"{BASE_URL}/coins")
    return res.json()

def safe_format_number(value, decimals=2):
    """Safely format a number, handling None values"""
    if value is None:
        return "N/A"
    else:
        if decimals == 0:
            return f"{value:,.0f}"
        else:
            return f"{value:,.{decimals}f}"


def safe_format_percentage(value, decimals=1):
    """Safely format a percentage, handling None values"""
    if value is None:
        return "N/A"
    else:
        return f"{value:.{decimals}f}%"


def inject_css():
    st.markdown("""
        <style>
            /* Hide Streamlit default elements */
            .stApp > header {visibility: hidden;}
            .stApp > div:first-child {padding-top: 0;}
            
            /* Main container */
            .main .block-container {
                padding-top: 2rem;
                max-width: 1400px;
            }
            
            /* Custom card styling */
            .crypto-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 16px;
                padding: 2px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
            }
            
            .crypto-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 16px 48px rgba(0,0,0,0.15);
            }
            
            .coin-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 16px;
                padding-bottom: 12px;
                border-bottom: 2px solid #f0f0f0;
            }
            
            .coin-title {
                font-size: 20px;
                font-weight: 700;
                color: #2d3748;
                margin: 0;
            }
            
            .coin-symbol {
                font-size: 14px;
                color: #718096;
                font-weight: 500;
            }
            
            .price-display {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 6px;
                border-radius: 8px;
                text-align: center;
                margin-bottom: 6px;
            }
            
            .price-label {
                font-size: 12px;
                opacity: 0.9;
            }
            
            .price-amount {
                font-size: 26px;
                font-weight: 800;
            }
            
            .stats-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px;
            margin-bottom: 10px;
            }
            
            .stat-box {
                background: #f8fafc;
                border-radius: 8px;
                padding: 6px;
                border-left: 3px solid #667eea;
            }
            
            .stat-title {
                font-size: 12px;
                color: #718096;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 3px;
            }
            
            .stat-number {
                font-size: 16px;
                font-weight: 700;
                color: #2d3748;
                margin: 0;
            }
            
            .positive { color: #48bb78; }
            .negative { color: #f56565; }
            
            .rank-indicator {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                
            .main .block-container {
            max-width: 1600px;  /* or even 1800px */
            padding: 1rem 2rem;
            }
            }
        </style>
    """, unsafe_allow_html=True)

def render_coin_card(coin):
    coin_name = coin.get('name', 'Unknown Coin')
    coin_symbol = coin.get('symbol', 'N/A')
    coin_price = coin.get('price', 0)
    coin_rank = coin.get('rank', 'N/A')
    coin_id = coin.get('coin_id', '')
    coin_image = coin.get('coin_image_url', '')

    ath_formatted = safe_format_number(coin.get('ath', 0), 2)
    percent_from_ath = coin.get('percent_from_ath')
    percent_formatted = safe_format_percentage(percent_from_ath)
    market_cap_formatted = safe_format_number(coin.get('market_cap', 0), 0)
    volume_formatted = safe_format_number(coin.get('volume_24h', 0), 0)
    price_formatted = safe_format_number(coin_price, 2)
    total_supply_formatted = safe_format_number(coin.get('total_supply', 0), 0)

    ath_color_class = "positive" if percent_from_ath is not None and percent_from_ath >= 0 else "negative"

    with st.container():
        st.markdown('<div class="crypto-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-inner">', unsafe_allow_html=True)

        # Top section
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div>
                    <h3 style="margin: 0; font-size: 22px;">{coin_name}</h3>
                    <p style="margin: 0; color: #999; font-size: 16px;">{coin_symbol}</p>
                </div>
                <div>
                    <img src="{coin_image}" width="42">
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Price display
        st.markdown(f"""
            <div class="price-display">
                <div class="price-label">Current Price</div>
                <div class="price-amount">${price_formatted}</div>
            </div>
        """, unsafe_allow_html=True)

        # Stats
        st.markdown(f"""
            <div class="stats-container">
                <div class="stat-box">
                    <div class="stat-title">Rank</div>
                    <div class="stat-number">#{coin_rank}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-title">Total Supply</div>
                    <div class="stat-number">{total_supply_formatted}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-title">ATH</div>
                    <div class="stat-number">${ath_formatted}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-title">% from ATH</div>
                    <div class="stat-number {ath_color_class}">{percent_formatted}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-title">Market Cap</div>
                    <div class="stat-number">${market_cap_formatted}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-title">24h Volume</div>
                    <div class="stat-number">${volume_formatted}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Buy section
        col1, col2 = st.columns([3, 1])
        with col1:
            quantity = st.number_input(
                f"Qty ({coin_symbol})", 
                key=f"qty_{coin_id}", 
                min_value=1, 
                step=1, 
                format="%d",
                label_visibility='collapsed'
            )
        with col2:
            if st.button("Buy", key=f"buy_{coin_id}", use_container_width=True, type='primary'):
                total = quantity * coin_price
                st.toast(f"✅ Bought {quantity} {coin_symbol} for ${total:,.2f}", icon="💸")

        st.markdown('</div></div>', unsafe_allow_html=True)




def show_buy_popup(coin):
    # Safely get values
    coin_name = coin.get('name', 'Unknown Coin')
    coin_symbol = coin.get('symbol', 'N/A')
    coin_price = coin.get('price', 0)
    coin_rank = coin.get('rank', 'N/A')
    coin_id = coin.get('coin_id', '')
    coin_image = coin.get('coin_image_url', '')
    
    st.markdown("---")
    st.markdown(f"## 🛒 Buy {coin_name}")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if coin_image:
            st.image(coin_image, width=80)
        st.markdown(f"**Current Price:** ${safe_format_number(coin_price, 2)}")
        st.markdown(f"**Rank:** #{coin_rank}")
        
        quantity = st.number_input(
            "Enter quantity:", 
            min_value=0.0, 
            step=0.01, 
            key=f"qty_{coin_id}"
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🚀 Confirm Purchase", key=f"confirm_{coin_id}", use_container_width=True):
                if coin_price and coin_price > 0:
                    total_cost = quantity * coin_price
                    st.success(f"✅ Successfully purchased {quantity} {coin_symbol} for ${total_cost:,.2f}")
                else:
                    st.success(f"✅ Successfully purchased {quantity} {coin_symbol}")
                st.balloons()
                # Clear the buy popup state
                st.session_state[f"show_buy_{coin_id}"] = False
                st.rerun()
        
        with col_b:
            if st.button("❌ Cancel", key=f"cancel_{coin_id}", use_container_width=True):
                st.session_state[f"show_buy_{coin_id}"] = False
                st.rerun()

def main():
    st.set_page_config(
        page_title="Crypto Dashboard", 
        layout="wide",
        page_icon="💹"
    )
    
    # Custom header
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 3rem;
                font-weight: 800;
                margin-bottom: 0.5rem;
            ">💹 Crypto Dashboard</h1>
            <p style="color: #718096; font-size: 1.2rem; margin: 0;">Top 20 Cryptocurrencies</p>
        </div>
    """, unsafe_allow_html=True)

    inject_css()

    coins = fetch_coins()
        
        # Check if any buy popup should be shown first
    active_popup = None
    for coin in coins:
            coin_id = coin.get('coin_id', '')
            if st.session_state.get(f"show_buy_{coin_id}", False):
                active_popup = coin
                break
        
    if active_popup:
            show_buy_popup(active_popup)
    else:
            # Display coins in rows of 3
            for i in range(0, len(coins), 4):
                cols = st.columns(4)
                for j, col in enumerate(cols):
                    if i + j < len(coins):
                        with col:
                            coin = coins[i + j]
                            render_coin_card(coin)
                            
if __name__ == "__main__":
    main()