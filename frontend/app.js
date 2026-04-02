document.addEventListener('DOMContentLoaded', () => {
    const personaCards = document.querySelectorAll('.persona-card');
    const findBtn = document.getElementById('findBtn');
    const personaBadge = document.getElementById('personaBadge');
    const resultsContainer = document.getElementById('resultsContainer');
    const locationInput = document.getElementById('locationInput');
    const btnText = findBtn.querySelector('.btn-text');
    const loader = findBtn.querySelector('.loader');

    let currentPersona = 'general';

    personaCards.forEach(card => {
        card.addEventListener('click', () => {
            personaCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            currentPersona = card.dataset.value;
            // Clean out the emoji for the badge
            const targetText = card.textContent.trim().replace(/[\u{1F300}-\u{1F9FF}]/gu, '').trim();
            personaBadge.textContent = 'Persona: ' + targetText;
        });
    });

    findBtn.addEventListener('click', async () => {
        const location = locationInput.value || 'Global';
        
        btnText.classList.add('hidden');
        loader.classList.remove('hidden');
        findBtn.disabled = true;
        
        try {
            const res = await fetch('/api/recommend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ location, user_type: currentPersona })
            });
            
            if (!res.ok) throw new Error('API Error: Make sure you ran scraper.py first!');
            const data = await res.json();
            
            renderResults(data);
        } catch (err) {
            resultsContainer.innerHTML = `<div class="empty-state" style="color:var(--warning)">${err.message}</div>`;
        } finally {
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
            findBtn.disabled = false;
        }
    });

    function renderResults(hotels) {
        if (!hotels.length) {
            resultsContainer.innerHTML = '<div class="empty-state">No hotels found.</div>';
            return;
        }

        resultsContainer.innerHTML = '';
        hotels.forEach((hotel, idx) => {
            const tags = hotel.highlights.map(h => `<span class="hl-tag">${h}</span>`).join('');
            
            let scoreColor = '--success';
            if(hotel.score < 7.0) scoreColor = '--warning';
            
            const card = document.createElement('div');
            card.className = 'hotel-card';
            card.style.animationDelay = `${idx * 0.1}s`;
            
            card.innerHTML = `
                <div class="hotel-info">
                    <h3>#${idx+1} ${hotel.hotel_name}</h3>
                    <p class="hotel-reason">💡 ${hotel.reason_for_recommendation}</p>
                    <div class="highlights">
                        ${tags}
                    </div>
                </div>
                <div class="hotel-score">
                    <div class="score-circle" style="--score: ${hotel.score * 10}; --success: var(${scoreColor})">
                        <span class="score-value">${hotel.score}</span>
                    </div>
                    <div class="metrics-row">
                        <span>Sentiment: ${hotel.metrics.sentiment_value > 0 ? '+' : ''}${hotel.metrics.sentiment_value}</span>
                        <span>Fake Risk: ${hotel.metrics.fake_risk_score}</span>
                    </div>
                </div>
            `;
            resultsContainer.appendChild(card);
        });
    }
});
