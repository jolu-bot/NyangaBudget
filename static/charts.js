/* ==================== NYANGABUDGET CHARTS.JS MODERNE ==================== */

// Configuration globale Chart.js
Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
Chart.defaults.font.size = 14;
Chart.defaults.color = '#666';
Chart.defaults.plugins.legend.display = true;
Chart.defaults.plugins.legend.position = 'bottom';
Chart.defaults.animation.duration = 1000;
Chart.defaults.animation.easing = 'easeInOutQuart';

// Gradients modernes
const gradients = {
    primary: ['rgba(102, 126, 234, 0.8)', 'rgba(118, 75, 162, 0.8)'],
    success: ['rgba(17, 153, 142, 0.8)', 'rgba(56, 239, 125, 0.8)'],
    danger: ['rgba(235, 51, 73, 0.8)', 'rgba(244, 92, 67, 0.8)'],
    warning: ['rgba(240, 147, 251, 0.8)', 'rgba(245, 87, 108, 0.8)'],
    info: ['rgba(79, 172, 254, 0.8)', 'rgba(0, 242, 254, 0.8)']
};

// Créer un gradient
function createGradient(ctx, colors) {
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, colors[0]);
    gradient.addColorStop(1, colors[1]);
    return gradient;
}

// ==================== GRAPHIQUE DÉPENSES VS REVENUS ====================
function createIncomeExpenseChart(canvasId, labels, expensesData, incomeData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Dépenses',
                    data: expensesData,
                    backgroundColor: createGradient(ctx.getContext('2d'), gradients.danger),
                    borderColor: 'rgba(235, 51, 73, 1)',
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false
                },
                {
                    label: 'Revenus',
                    data: incomeData,
                    backgroundColor: createGradient(ctx.getContext('2d'), gradients.success),
                    borderColor: 'rgba(17, 153, 142, 1)',
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        font: {
                            size: 14,
                            weight: '600'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    cornerRadius: 8,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + 
                                   new Intl.NumberFormat('fr-FR', { 
                                       style: 'currency', 
                                       currency: 'XAF' 
                                   }).format(context.parsed.y);
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            weight: '600'
                        }
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        callback: function(value) {
                            return new Intl.NumberFormat('fr-FR', { 
                                style: 'currency', 
                                currency: 'XAF',
                                notation: 'compact',
                                compactDisplay: 'short'
                            }).format(value);
                        }
                    }
                }
            },
            animation: {
                duration: 1500,
                easing: 'easeInOutQuart',
                onComplete: function() {
                    // Animation terminée
                }
            }
        }
    });
    
    return chart;
}

// ==================== GRAPHIQUE EN DONUT (CATÉGORIES) ====================
function createCategoryDonutChart(canvasId, labels, data, colors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    const chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors || [
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(17, 153, 142, 0.8)',
                    'rgba(235, 51, 73, 0.8)',
                    'rgba(240, 147, 251, 0.8)',
                    'rgba(79, 172, 254, 0.8)',
                    'rgba(255, 159, 64, 0.8)',
                    'rgba(153, 102, 255, 0.8)'
                ],
                borderWidth: 3,
                borderColor: '#fff',
                hoverOffset: 15
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '65%',
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        padding: 15,
                        usePointStyle: true,
                        font: {
                            size: 13,
                            weight: '600'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            
                            return label + ': ' + 
                                   new Intl.NumberFormat('fr-FR', { 
                                       style: 'currency', 
                                       currency: 'XAF' 
                                   }).format(value) + 
                                   ' (' + percentage + '%)';
                        }
                    }
                }
            },
            animation: {
                animateRotate: true,
                animateScale: true,
                duration: 1500
            }
        }
    });
    
    return chart;
}

// ==================== GRAPHIQUE EN LIGNE (TENDANCES) ====================
function createTrendLineChart(canvasId, labels, data, label, gradientColors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    const gradient = createGradient(ctx.getContext('2d'), gradientColors || gradients.primary);
    
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                borderColor: gradientColors ? gradientColors[0] : 'rgba(102, 126, 234, 1)',
                backgroundColor: gradient,
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#fff',
                pointBorderColor: gradientColors ? gradientColors[0] : 'rgba(102, 126, 234, 1)',
                pointBorderWidth: 3,
                pointRadius: 5,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + 
                                   new Intl.NumberFormat('fr-FR', { 
                                       style: 'currency', 
                                       currency: 'XAF' 
                                   }).format(context.parsed.y);
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        callback: function(value) {
                            return new Intl.NumberFormat('fr-FR', { 
                                style: 'currency', 
                                currency: 'XAF',
                                notation: 'compact'
                            }).format(value);
                        }
                    }
                }
            }
        }
    });
    
    return chart;
}

// ==================== GRAPHIQUE RADAR (ANALYSE MULTI-CRITÈRES) ====================
function createRadarChart(canvasId, labels, datasets) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    const chart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: datasets.map((dataset, index) => ({
                label: dataset.label,
                data: dataset.data,
                backgroundColor: `rgba(${index * 50 + 100}, ${index * 30 + 120}, ${234 - index * 40}, 0.2)`,
                borderColor: `rgba(${index * 50 + 100}, ${index * 30 + 120}, ${234 - index * 40}, 1)`,
                borderWidth: 2,
                pointBackgroundColor: `rgba(${index * 50 + 100}, ${index * 30 + 120}, ${234 - index * 40}, 1)`,
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: `rgba(${index * 50 + 100}, ${index * 30 + 120}, ${234 - index * 40}, 1)`
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    ticks: {
                        backdropColor: 'transparent'
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
    
    return chart;
}

// ==================== UTILITAIRES ====================

// Formater les montants
function formatCurrency(amount) {
    return new Intl.NumberFormat('fr-FR', { 
        style: 'currency', 
        currency: 'XAF' 
    }).format(amount);
}

// Animer les nombres
function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = formatCurrency(Math.round(current));
    }, 16);
}

// Export des fonctions
window.NyangaCharts = {
    createIncomeExpenseChart,
    createCategoryDonutChart,
    createTrendLineChart,
    createRadarChart,
    formatCurrency,
    animateValue
};
