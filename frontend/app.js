document.addEventListener('DOMContentLoaded', () => {
    const personaCards = document.querySelectorAll('.persona-card');
    const findBtn = document.getElementById('findBtn');
    const personaBadge = document.getElementById('personaBadge');
    const resultsContainer = document.getElementById('resultsContainer');
    const locationInput = document.getElementById('locationInput');
    const btnText = findBtn.querySelector('.btn-text');
    const loader = findBtn.querySelector('.loader');
    const sidebar = document.getElementById('sidebar');
    const menuToggle = document.getElementById('menuToggle');

    let currentPersona = 'general';

    // Mobile Menu Toggle
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            menuToggle.textContent = sidebar.classList.contains('open') ? '✕' : '☰';
        });
    }

    // Auto-clear location input on focus
    locationInput.addEventListener('focus', () => {
        if (locationInput.value === 'Global') {
            locationInput.value = '';
        }
    });

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
        
        // UI Loading State
        btnText.classList.add('hidden');
        loader.classList.remove('hidden');
        findBtn.disabled = true;
        showShimmer();
        
        try {
            const res = await fetch('/api/recommend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ location, user_type: currentPersona })
            });
            
            if (!res.ok) throw new Error('API Error: Ensure the server is running and data is generated.');
            const data = await res.json();
            
            setTimeout(() => {
                renderResults(data);
                hideShimmer();
            }, 600); // Small artificial delay for shimmer feel
        } catch (err) {
            resultsContainer.innerHTML = `<div class="empty-state" style="color:var(--warning)">${err.message}</div>`;
            hideShimmer();
        } finally {
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
            findBtn.disabled = false;
        }
    });

    function showShimmer() {
        resultsContainer.innerHTML = `
            <div class="shimmer-card"></div>
            <div class="shimmer-card"></div>
            <div class="shimmer-card"></div>
        `;
    }

    function hideShimmer() {
        // Results rendering handles this
    }

    function renderResults(hotels) {
        if (!hotels.length) {
            resultsContainer.innerHTML = '<div class="empty-state">No hotels found matching criteria.</div>';
            return;
        }

        resultsContainer.innerHTML = '';
        hotels.forEach((hotel, idx) => {
            const tags = hotel.highlights.map(h => `<span class="hl-tag">${h}</span>`).join('');
            const chartId = `chart-${idx}`;
            
            let scoreColor = '--success';
            if(hotel.score < 7.0) scoreColor = '--warning';
            
            const card = document.createElement('div');
            card.className = 'hotel-card';
            card.style.animationDelay = `${idx * 0.1}s`;
            
            card.innerHTML = `
                <div class="card-top">
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
                </div>
                <div class="chart-container">
                    <canvas id="${chartId}"></canvas>
                </div>
            `;
            resultsContainer.appendChild(card);
            
            // Render Chart for this hotel
            renderHotelChart(chartId, hotel);
        });
    }

    function renderHotelChart(canvasId, hotel) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        // Mock data distribution based on logical scores for visual interest
        const baseScore = hotel.score;
        const sentiment = (hotel.metrics.sentiment_value + 1) * 5; // Scale to 10
        const trust = (1 - hotel.metrics.fake_risk_score) * 10;
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Rating', 'Sentiment', 'Trust', 'Location', 'Value'],
                datasets: [{
                    label: 'Attribute Breakdown',
                    data: [baseScore, sentiment, trust, Math.random() * 4 + 6, Math.random() * 3 + 7],
                    backgroundColor: [
                        '#6366f1', '#22d3ee', '#10b981', '#f59e0b', '#ec4899'
                    ],
                    borderRadius: 4
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' }, max: 10 },
                    y: { grid: { display: false }, ticks: { color: '#f1f5f9' } }
                }
            }
        });
    }
});
