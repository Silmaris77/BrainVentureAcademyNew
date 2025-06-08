import streamlit as st

def m3_fixed_card(title, content, badge=None, icon=None):
    """Prosta karta naprawiająca problem z renderowaniem HTML"""    # Dodajemy style CSS
    st.markdown("""
    <style>
    .fixed-card-container {
        background-color: white;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        position: relative;
        max-width: 100%;
    }
    
    .fixed-card-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #2196F3, #673AB7);
    }
    
    .fixed-card-title {
        font-size: 1.3rem;
        font-weight: 500;
        color: #1A237E;
        margin-bottom: 16px;
        line-height: 1.3;
    }
    
    .fixed-card-content {
        font-size: 1rem;
        color: #555;
        line-height: 1.6;
        text-align: justify;
        margin-bottom: 12px;
    }
    
    .fixed-card-content p {
        margin-bottom: 0.8rem;
    }
    
    .fixed-card-content br + br {
        display: block;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Tworzymy HTML karty
    card_html = f"""
    <div class="fixed-card-container">
        <div class="fixed-card-title">{icon + ' ' if icon else ''}{title}</div>
        <div class="fixed-card-content">{content}</div>
        {f'<div style="margin-top:12px; text-align: right;"><span style="background-color: #673AB7; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.8rem;">{badge}</span></div>' if badge else ''}
    </div>
    """
    
    # Renderujemy kartę
    st.markdown(card_html, unsafe_allow_html=True)
