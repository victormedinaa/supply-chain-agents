/**
 * Supply Chain Command Center - Main Application
 * Handles navigation, data simulation, and UI updates.
 */

(function () {
    'use strict';

    // DOM Elements
    const navItems = document.querySelectorAll('.nav-item');
    const pageTitle = document.querySelector('.page-title h1');
    const breadcrumb = document.querySelector('.breadcrumb');

    // Agent data for simulation
    const agentTasks = {
        'Inventory Agent': [
            'Analyzing stock levels',
            'Calculating safety stock',
            'Processing reorder alerts',
            'Updating demand forecast'
        ],
        'Procurement Agent': [
            'Negotiating with suppliers',
            'Evaluating quotes',
            'Processing purchase orders',
            'Risk assessment pending'
        ],
        'Finance Agent': [
            'Budget variance check',
            'Cost analysis running',
            'Approving transactions',
            'Generating reports'
        ],
        'Logistics Agent': [
            'Route optimization',
            'Tracking shipments',
            'Carrier performance review',
            'Transit time analysis'
        ],
        'Quality Agent': [
            'SPC monitoring',
            'Inspection queue review',
            'Defect trend analysis',
            'Supplier audit pending'
        ],
        'Production Agent': [
            'Scheduling queue',
            'Capacity planning',
            'Material requirement check',
            'Line allocation'
        ]
    };

    // Activity messages for simulation
    const activityTemplates = [
        { dot: 'procurement', text: 'Procurement Agent negotiated {percent}% discount with {supplier}' },
        { dot: 'logistics', text: 'Shipment {shipment} cleared customs in {location}' },
        { dot: 'quality', text: 'Quality inspection passed for Batch {batch}' },
        { dot: 'inventory', text: '{sku} below reorder point. PO generated.' },
        { dot: 'production', text: 'Production order {order} completed' },
        { dot: 'finance', text: 'Budget variance report generated for Q{quarter}' }
    ];

    const suppliers = ['Global Steel 7', 'TechParts Asia', 'EuroComponent GmbH', 'Pacific Motors'];
    const locations = ['Rotterdam', 'Singapore', 'Los Angeles', 'Shanghai'];

    // Initialize
    function init() {
        setupNavigation();
        startAgentSimulation();
        startMetricsUpdate();
    }

    // Navigation handling
    function setupNavigation() {
        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();

                // Update active state
                navItems.forEach(nav => nav.classList.remove('active'));
                item.classList.add('active');

                // Update page title
                const viewName = item.querySelector('span:last-child').textContent;
                pageTitle.textContent = viewName;

                // Update breadcrumb
                const descriptions = {
                    'Dashboard': 'Overview of supply chain operations',
                    'Agents': 'Monitor autonomous agent activity',
                    'Inventory': 'Stock levels and warehouse management',
                    'Logistics': 'Shipment tracking and route optimization',
                    'Suppliers': 'Supplier performance and relationships',
                    'Alerts': 'Active alerts and notifications'
                };
                breadcrumb.textContent = descriptions[viewName] || '';
            });
        });
    }

    // Simulate agent task updates
    function startAgentSimulation() {
        const agentCards = document.querySelectorAll('.agent-card');

        setInterval(() => {
            agentCards.forEach(card => {
                const nameEl = card.querySelector('.agent-name');
                const taskEl = card.querySelector('.agent-task');
                const timeEl = card.querySelector('.agent-time');

                const agentName = nameEl.textContent;
                const tasks = agentTasks[agentName];

                if (tasks && Math.random() > 0.7) {
                    const newTask = tasks[Math.floor(Math.random() * tasks.length)];
                    taskEl.textContent = newTask;
                    timeEl.textContent = 'just now';
                }
            });
        }, 3000);

        // Update time displays
        setInterval(() => {
            const timeEls = document.querySelectorAll('.agent-time');
            timeEls.forEach(el => {
                const current = el.textContent;
                if (current === 'just now') {
                    el.textContent = '2s ago';
                } else {
                    const match = current.match(/(\d+)s ago/);
                    if (match) {
                        const seconds = parseInt(match[1]) + Math.floor(Math.random() * 3) + 1;
                        if (seconds < 60) {
                            el.textContent = `${seconds}s ago`;
                        } else {
                            el.textContent = '1m ago';
                        }
                    }
                }
            });
        }, 2000);
    }

    // Simulate metric updates
    function startMetricsUpdate() {
        const inventoryValue = document.querySelectorAll('.metric-value')[1];
        const shipments = document.querySelectorAll('.metric-value')[2];
        const onTime = document.querySelectorAll('.metric-value')[3];

        setInterval(() => {
            // Small random fluctuations
            if (Math.random() > 0.8) {
                const base = 52.7 + (Math.random() - 0.5) * 2;
                inventoryValue.textContent = `$${base.toFixed(1)}M`;
            }

            if (Math.random() > 0.9) {
                const base = 127 + Math.floor((Math.random() - 0.5) * 10);
                shipments.textContent = base.toString();
            }

            if (Math.random() > 0.85) {
                const base = 94.2 + (Math.random() - 0.5) * 1;
                onTime.textContent = `${base.toFixed(1)}%`;
            }
        }, 5000);
    }

    // Helper functions
    function randomItem(arr) {
        return arr[Math.floor(Math.random() * arr.length)];
    }

    function formatNumber(num) {
        return num.toString().padStart(4, '0');
    }

    // Start the application
    document.addEventListener('DOMContentLoaded', init);
})();
