Product Requirements Document (PRD): Personal Finance and Investment Insights App
1. Overview
1.1 Purpose
The Personal Finance and Investment Insights App ("the App") is a single-user SaaS platform designed to help the user manage personal finances by uploading financial data (OFX, CSV, QIF files), reconciling transactions in a Xero-inspired interface, and storing data in Supabase. The App provides a dashboard for spending insights, budgeting, and savings goals, leveraging Grok 3 to offer personalized advice for a reckless spender (e.g., cutting alcohol expenses, managing high-interest debt). It includes a Money Trends page for beginner-friendly investment education, market tracking (stocks, crypto, gold), and investment simulations, with plans to evolve into an "investment buddy."
1.2 Background
The user needs a tool to track finances due to reckless spending habits. Existing solutions like Xero are too business-focused, while consumer apps lack deep AI insights or investment education. The App combines simple reconciliation, AI-driven advice via Grok 3, and dynamic investment learning to improve financial health.
1.3 Scope
The App is initially for a single user (the owner) with potential for multi-user scaling later. The MVP includes:
File uploads (OFX, CSV, QIF) for transaction data.
Xero-style reconciliation with manual and ML-based categorization.
Supabase storage for transactions and accounts.
Dashboard with spending charts, budgets, and savings goals.
Grok 3 insights for spending reduction and basic investment tips.
Money Trends page with tutorials, market tracking, and simulations.
Python backend, React frontend with Xero-inspired UI.
Legal/compliance (e.g., GDPR, investment disclaimers) will be addressed post-MVP.
1.4 Assumptions
OFX files may have quirks (e.g., missing fields, non-standard dates), requiring testing during development.
Supabase free tier is sufficient for initial storage needs.
Grok 3 API access is available via xAI.
Market data APIs (e.g., Alpha Vantage, CoinGecko) provide reliable stock/crypto/gold prices.
The user will provide sample OFX/CSV/QIF files for backend testing.
2. Objectives
2.1 Business Goals
Enable the user to track and reconcile transactions.
Reduce reckless spending by providing actionable Grok 3 insights (e.g., "Cut alcohol to save $200/month").
Educate the user on investments (stocks, crypto, gold) to build savings confidence.
Create a scalable codebase for potential multi-user SaaS expansion.
2.2 User Goals
Upload financial data easily and reconcile transactions like in Xero.
Visualize spending patterns, set budgets, and track savings goals.
Receive tailored advice to curb overspending (e.g., alcohol, high-interest debt).
Learn about investing as a beginner, track markets, and simulate investments.
Use a clean, Xero-inspired UI for intuitive navigation.
3. Requirements
3.1 Functional Requirements
3.1.1 File Upload and Parsing
Description: Users upload OFX, CSV, or QIF files containing transaction data from multiple bank accounts.
Details:
Extract:
Bank account name
Transaction date
Description (payee, memo)
Amount (positive for deposits, negative for withdrawals)
Transaction type (e.g., debit, credit)
Transaction ID (if available)
Support multiple accounts per file.
Handle CSV/QIF with flexible column mapping (e.g., user selects "date" column).
Display errors for invalid files (e.g., corrupt OFX, missing headers in CSV).
Priority: High (core feature for MVP).
3.1.2 Reconciliation
Description: Users reconcile transactions in a Xero-inspired table view.
Details:
Display transactions with columns: date, description, amount, category, reconciled status.
Allow manual categorization (e.g., groceries, utilities).
Support transaction splitting (e.g., $100 → $60 groceries, $40 dining).
Add notes/tags for tracking.
Suggest categories using ML (e.g., "Walmart" → Groceries) beyond Grok 3.
Auto-reconcile based on user-defined rules (e.g., "Amazon → Shopping").
Highlight unreconciled transactions.
Priority: High (core feature for MVP).
3.1.3 Supabase Storage
Description: Store transaction data in a Supabase PostgreSQL database.
Details:
Tables:
accounts: account ID, name, type (checking, savings, credit).
transactions: transaction ID, account ID, date, description, amount, category, reconciled status, tags, notes.
categories: category ID, name, user-defined flag.
budgets: budget ID, category ID, amount, period (monthly).
goals: goal ID, name, target amount, current amount, deadline.
Enable real-time updates for UI refresh.
Use row-level security (RLS) for future multi-user support.
Priority: High (core feature for MVP).
3.1.4 Dashboard
Description: Display financial insights, budgets, and goals.
Details:
Charts:
Pie chart: Spending by category (e.g., groceries, dining).
Line chart: Monthly spending vs. income.
Bar chart: Cash flow (net income minus expenses).
Gauge: Progress toward savings goals.
Metrics:
Total account balances.
Unreconciled transaction count.
Top spending categories.
Budgets: Set monthly limits per category (e.g., $200 dining).
Savings Goals: Track progress (e.g., "$5,000 emergency fund").
Anomalies: Highlight unusual spending (e.g., "Dining up 50% this month").
Priority: High (core feature for MVP).
3.1.5 Grok 3 Integration
Description: Use Grok 3 to analyze transactions and provide insights.
Details:
Insights for reckless spending:
Budget cuts (e.g., "Stop drinking to save $300/month").
Debt management (e.g., "High interest rates; pay off $1,000 credit card").
Savings tips (e.g., "Gold is up 5%; invest $100?").
Access market data for investment suggestions.
Chatbot UI for queries (e.g., "How do I save more?").
Cache responses to reduce API calls.
Priority: Medium (MVP includes basic insights).
3.1.6 Money Trends Page
Description: Educate on investments and track markets.
Details:
Split layout:
Left: Beginner tutorials (e.g., "What is a stock?").
Right: Market data and watchlist.
Tutorials:
Start beginner-level; adapt to intermediate based on user interaction (e.g., repeat visits trigger deeper topics).
Cover stocks, crypto, gold, ETFs.
Market Tracking:
Dynamic assets (user adds stocks, coins, commodities).
Charts for daily/weekly/monthly performance.
News feed via APIs (e.g., Alpha Vantage, CoinGecko).
Simulations:
Calculate past returns (e.g., "$1,000 in Bitcoin last year → $1,200").
Hypothetical portfolios (e.g., "50% stocks, 50% gold").
Grok 3 insights (e.g., "Crypto is volatile; diversify").
Priority: Medium (MVP includes basic tutorials and tracking).
3.1.7 User Interface
Description: Xero-inspired UI with navigation.
Details:
Main Page: Links to Dashboard, Reconciliation, Money Trends, Upload, Settings.
Reconciliation Page: Table with filters (date, category).
Dashboard Page: Chart-heavy with budget/goal widgets.
Money Trends Page: Split-pane (tutorials, markets).
Settings: Manage accounts, categories, budgets, goals.
Responsive for desktop/mobile.
Priority: High (core feature for MVP).
3.2 Non-Functional Requirements
3.2.1 Performance
Process 1,000 transactions in <3 seconds for uploads.
Load dashboard charts in <2 seconds.
3.2.2 Scalability
Support single-user MVP; design database for 1,000+ users later.
Use Supabase and FastAPI for horizontal scaling.
3.2.3 Security
Encrypt file uploads (HTTPS).
Sanitize inputs to prevent XSS/SQL injection.
Use Supabase RLS for data isolation.
Store no sensitive bank details (e.g., account numbers).
3.2.4 Availability
Target 99.9% uptime via Supabase/Vercel.
3.2.5 Usability
Xero-like UI: Clean, minimal, blue/white color scheme.
Mobile-responsive with touch-friendly controls.
4. Technical Architecture
4.1 Backend
Framework: FastAPI (Python) for RESTful API.
Libraries:
ofxparse: Parse OFX files.
pandas: Handle CSV/QIF parsing.
qifparse: Parse QIF files.
supabase-py: Supabase client.
scikit-learn: ML for category suggestions.
Endpoints:
POST /upload: Upload and parse files.
GET /transactions: List transactions with filters.
PUT /transactions/{id}: Update category/reconciled status.
POST /insights: Query Grok 3 for advice.
GET /markets: Fetch market data.
Deployment: Vercel or Render.
4.2 Frontend
Framework: React with TypeScript.
Libraries:
Chart.js: Charts for dashboard/Money Trends.
Tailwind CSS: Xero-inspired styling.
React-Table: Reconciliation table.
Dropzone.js: File uploads.
Components:
Dashboard: Chart widgets, budget/goal trackers.
ReconciliationTable: Filterable transaction grid.
MoneyTrends: Split-pane for tutorials/markets.
Chatbot: Floating Grok 3 query box.
Deployment: Netlify or Vercel.
4.3 Database
Platform: Supabase (PostgreSQL).
Schema:
sql
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT CHECK (type IN ('checking', 'savings', 'credit'))
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    is_custom BOOLEAN DEFAULT FALSE
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id),
    date DATE NOT NULL,
    description TEXT,
    amount DECIMAL(10,2) NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    reconciled BOOLEAN DEFAULT FALSE,
    tags TEXT[],
    notes TEXT
);

CREATE TABLE budgets (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id),
    amount DECIMAL(10,2) NOT NULL,
    period TEXT CHECK (period = 'monthly')
);

CREATE TABLE goals (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    target_amount DECIMAL(10,2) NOT NULL,
    current_amount DECIMAL(10,2) DEFAULT 0,
    deadline DATE
);
Indexes:
transactions.date, transactions.account_id.
categories.name.
4.4 External APIs
Grok 3: xAI API for insights.
Market Data:
Alpha Vantage: Stocks.
CoinGecko: Crypto.
Kitco: Gold/commodities.
Cache: Redis or Supabase edge functions for API responses.
5. User Flow
Onboarding:
User configures accounts and default categories.
File Upload:
Upload OFX/CSV/QIF; map columns for CSV/QIF.
View parsed transactions or error messages.
Reconciliation:
See transactions in table.
Assign categories manually or use ML suggestions.
Mark reconciled or split transactions.
Dashboard:
View spending charts, budgets, and goals.
Adjust limits or track progress.
Grok 3 Insights:
Read tips (e.g., "Cut alcohol to save $300").
Query chatbot (e.g., "Pay off debt?").
Money Trends:
Read tutorials (e.g., "What is crypto?").
Track assets and simulate investments.
Add assets to watchlist.
6. Development Plan
Phase 1: Backend and File Parsing
Set up FastAPI and Supabase.
Implement OFX/CSV/QIF parsing (ofxparse, pandas, qifparse).
Store transactions in Supabase.
Test with sample files.
Phase 2: Reconciliation and Frontend
Build reconciliation API (categorization, rules).
Create React UI with transaction table.
Add ML category suggestions (scikit-learn).
Style with Tailwind (Xero-like).
Phase 3: Dashboard and Budgets
Add dashboard API for charts/metrics.
Build React components for pie/line/bar charts.
Implement budgets and goals in Supabase/UI.
Phase 4: Grok 3 and Money Trends
Integrate Grok 3 API for spending insights.
Add chatbot UI.
Build Money Trends with tutorials, market APIs, and simulations.
Phase 5: Polish and Launch
Optimize performance (e.g., cache market data).
Test mobile responsiveness.
Deploy to Vercel/Netlify.
Deliver MVP.
7. Success Metrics
MVP launched successfully.
Reconcile 100+ transactions accurately.
Grok 3 suggests 5+ actionable insights (e.g., spending cuts).
Money Trends tracks 3+ assets with simulations.
User reports improved financial awareness (subjective).
8. Risks and Mitigations
Risk: OFX file quirks break parsing.
Mitigation: Test with multiple sample files; support CSV/QIF.
Risk: Grok 3 API limits or delays.
Mitigation: Cache responses; fallback to static tips.
Risk: Market API costs or downtime.
Mitigation: Use free tiers; cache data.
Risk: Development delays.
Mitigation: Prioritize file upload and reconciliation for early wins.
9. Future Considerations
Scale to multi-user SaaS with subscriptions.
Add direct bank feeds (if bank supports).
Implement GDPR/CCPA compliance.
Add advanced investment features (e.g., portfolio management). 