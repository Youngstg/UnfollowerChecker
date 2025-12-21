// Check followers function
async function checkFollowers() {
    const btn = document.getElementById('checkBtn');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');

    btn.disabled = true;
    loading.style.display = 'block';
    result.style.display = 'none';

    try {
        const response = await fetch('/check_followers');
        const data = await response.json();

        loading.style.display = 'none';

        if (data.error) {
            result.className = 'result-message error';
            result.textContent = 'Error: ' + data.error;
            result.style.display = 'block';
        } else {
            result.className = 'result-message success';
            result.innerHTML = `
                <strong>Berhasil!</strong><br>
                Followers: ${data.followers_count}<br>
                Following: ${data.following_count}<br>
                ${data.new_unfollowers.length > 0 ?
                    `<strong style="color: #c33;">Unfollowers baru: ${data.new_unfollowers.length}</strong> (${data.new_unfollowers.join(', ')})`
                    : 'Tidak ada unfollowers baru'}
            `;
            result.style.display = 'block';

            // Reload page after 2 seconds
            setTimeout(() => {
                location.reload();
            }, 2000);
        }
    } catch (error) {
        loading.style.display = 'none';
        result.className = 'result-message error';
        result.textContent = 'Error: ' + error.message;
        result.style.display = 'block';
    } finally {
        btn.disabled = false;
    }
}

// Load chart
async function loadChart() {
    try {
        const response = await fetch('/stats');
        const data = await response.json();

        if (data.error) {
            console.error('Error loading chart:', data.error);
            return;
        }

        const ctx = document.getElementById('followersChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.timestamps,
                datasets: [
                    {
                        label: 'Followers',
                        data: data.followers,
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Following',
                        data: data.following,
                        borderColor: '#764ba2',
                        backgroundColor: 'rgba(118, 75, 162, 0.1)',
                        tension: 0.4,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading chart:', error);
    }
}

// Load chart on page load
if (document.getElementById('followersChart')) {
    loadChart();
}
