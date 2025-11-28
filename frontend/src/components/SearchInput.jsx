import { useState } from 'react';
import { motion } from 'framer-motion';

export default function SearchInput({ onSearch, isLoading }) {
    const [query, setQuery] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim()) {
            onSearch(query);
        }
    };

    return (
        <motion.form
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
            onSubmit={handleSubmit}
            className="max-w-2xl mx-auto mb-12"
        >
            <div className="relative">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Ask anything (e.g., 'Is coffee good for you?')"
                    className="w-full px-6 py-4 text-lg rounded-full border border-slate-200 shadow-lg focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
                    disabled={isLoading}
                />
                <button
                    type="submit"
                    disabled={isLoading}
                    className="absolute right-2 top-2 bottom-2 px-6 bg-primary text-white rounded-full font-medium hover:bg-blue-600 transition-colors disabled:opacity-50"
                >
                    {isLoading ? 'Searching...' : 'Search'}
                </button>
            </div>
        </motion.form>
    );
}
