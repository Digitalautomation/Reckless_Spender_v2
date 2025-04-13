import React, { useState, useEffect } from 'react';

// Define interfaces
interface Category {
    id: number;
    name: string;
    // is_custom: boolean; // We might not need this field in the frontend directly yet
}

interface Transaction {
    id: number;
    account_id: number;
    date: string; // Dates usually come as strings from JSON
    description: string | null;
    amount: number; // Assuming backend converts Decimal to number/string
    category_id: number | null;
    reconciled: boolean;
    tags: string[] | null;
    notes: string | null;
    transaction_type: string | null;
    fitid: string | null;
}

function ReconciliationPage() {
    const [transactions, setTransactions] = useState<Transaction[]>([]);
    const [categories, setCategories] = useState<Category[]>([]); // State for categories
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    // Function to handle toggling the reconciled status
    const handleReconcileToggle = async (txId: number, newReconciledState: boolean) => {
        // 1. Optimistic UI Update
        const originalTransactions = [...transactions]; // Keep a copy for rollback
        setTransactions(currentTransactions =>
            currentTransactions.map(tx =>
                tx.id === txId ? { ...tx, reconciled: newReconciledState } : tx
            )
        );

        // 2. API Call
        try {
            const response = await fetch(`http://localhost:8000/transactions/${txId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ reconciled: newReconciledState }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `Failed to update transaction ${txId}`);
            }
            // Optional: Maybe add a temporary success message or visual cue
            console.log(`Transaction ${txId} reconciled status updated successfully.`);
            setError(null); // Clear previous errors on success

        } catch (err: any) {
            console.error("Failed to update reconcile status:", err);
            setError(`Error updating transaction ${txId}: ${err.message}. Reverting change.`);
            // 3. Rollback UI on error
            setTransactions(originalTransactions);
        }
    };

    // Function to handle changing the category
    const handleCategoryChange = async (txId: number, newCategoryId: number | null) => {
        console.log(`Changing category for tx ${txId} to ${newCategoryId}`); // Add log
        // 1. Optimistic UI Update
        const originalTransactions = [...transactions]; // Keep for rollback
        setTransactions(currentTransactions =>
            currentTransactions.map(tx =>
                tx.id === txId ? { ...tx, category_id: newCategoryId } : tx
            )
        );

        // 2. API Call
        try {
            const response = await fetch(`http://localhost:8000/transactions/${txId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                // Send category_id (can be null if "Uncategorized" is selected)
                body: JSON.stringify({ category_id: newCategoryId }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `Failed to update category for transaction ${txId}`);
            }
            console.log(`Transaction ${txId} category updated successfully.`);
            setError(null); // Clear previous errors

        } catch (err: any) {
            console.error("Failed to update category:", err);
            setError(`Error updating category for transaction ${txId}: ${err.message}. Reverting change.`);
            // 3. Rollback UI on error
            setTransactions(originalTransactions);
        }
    };

    // Fetch initial data (transactions and categories)
    useEffect(() => {
        const fetchData = async () => {
            setIsLoading(true);
            setError(null);
            let transactionsLoaded = false;
            let categoriesLoaded = false;
            
            try {
                // Fetch both concurrently
                const [transactionsResponse, categoriesResponse] = await Promise.all([
                    fetch('http://localhost:8000/transactions/'),
                    fetch('http://localhost:8000/categories/')
                ]);

                if (!transactionsResponse.ok) {
                    throw new Error(`Failed to fetch transactions: ${transactionsResponse.status}`);
                }
                const transactionsData: Transaction[] = await transactionsResponse.json();
                setTransactions(transactionsData);
                transactionsLoaded = true;

                if (!categoriesResponse.ok) {
                    throw new Error(`Failed to fetch categories: ${categoriesResponse.status}`);
                }
                const categoriesData: Category[] = await categoriesResponse.json();
                setCategories(categoriesData);
                categoriesLoaded = true;

            } catch (err: any) {
                console.error("Failed to fetch data:", err);
                setError(`Failed to load data: ${err.message}`);
            } finally {
                // Only set loading to false if both succeeded or an error occurred
                 if ((transactionsLoaded && categoriesLoaded) || error) {
                    setIsLoading(false);
                 }
            }
        };

        fetchData();
    }, []); // Empty dependency array means this runs once on mount

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Reconcile Transactions</h1>

            {isLoading && <p className="text-center text-gray-500 dark:text-gray-400">Loading transactions...</p>}
            {error && <p className="text-center text-red-500 dark:text-red-400">Error: {error}</p>}

            {!isLoading && !error && (
                <div className="overflow-x-auto shadow-md rounded-lg">
                    <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                        <thead className="bg-gray-50 dark:bg-gray-800">
                            <tr>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Date</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Description</th>
                                <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Amount</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Category</th>
                                <th scope="col" className="px-6 py-3 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Reconciled</th>
                                {/* Add more columns as needed later (e.g., Actions) */}
                            </tr>
                        </thead>
                        <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
                            {transactions.length > 0 ? (
                                transactions.map((tx) => (
                                    <tr key={tx.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50">
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">{tx.date}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">{tx.description || 'N/A'}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium 
                                                       ${tx.amount >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}">
                                            {/* Basic currency formatting - consider a library later */}
                                            {new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(tx.amount)}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                                            {/* Category Dropdown */}
                                            <select
                                                value={tx.category_id ?? ''} // Use empty string for 'Uncategorized' option value
                                                onChange={(e) => {
                                                    // Parse the value, allowing for the empty string ("Uncategorized")
                                                    const newCategoryId = e.target.value ? parseInt(e.target.value, 10) : null;
                                                    handleCategoryChange(tx.id, newCategoryId); // Ensure this line calls the handler
                                                }}
                                                className="block w-full p-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100 dark:focus:ring-offset-gray-800"
                                            >
                                                <option value="">Uncategorized</option> {/* Option for null category_id */}
                                                {categories.map(cat => (
                                                    <option key={cat.id} value={cat.id}>
                                                        {cat.name}
                                                    </option>
                                                ))}
                                            </select>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-center text-sm">
                                            {/* Interactive Checkbox */}
                                            <input 
                                                type="checkbox" 
                                                checked={tx.reconciled}
                                                onChange={(e) => handleReconcileToggle(tx.id, e.target.checked)}
                                                className="rounded border-gray-300 dark:border-gray-600 text-blue-600 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:checked:bg-blue-500 dark:checked:border-blue-500 cursor-pointer"
                                            />
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan={5} className="px-6 py-4 text-center text-sm text-gray-500 dark:text-gray-400">No transactions found.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}

export default ReconciliationPage; 