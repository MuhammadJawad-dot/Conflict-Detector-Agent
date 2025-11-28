import { motion } from 'framer-motion';

export default function Results({ googleResults, redditResults }) {
    return (
        <div className="grid md:grid-cols-2 gap-8 mb-12">
            {/* Google Results */}
            <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="space-y-4"
            >
                <h2 className="text-xl font-semibold flex items-center gap-2 text-slate-700">
                    <span className="text-2xl">🌍</span> Google Results
                </h2>
                {googleResults.map((result, index) => (
                    <div key={index} className="bg-white p-4 rounded-xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
                        <a href={result.link} target="_blank" rel="noopener noreferrer" className="text-primary font-medium hover:underline block mb-1">
                            {result.title}
                        </a>
                        <p className="text-sm text-slate-600 line-clamp-2">{result.snippet}</p>
                    </div>
                ))}
            </motion.div>

            {/* Reddit Results */}
            <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="space-y-4"
            >
                <h2 className="text-xl font-semibold flex items-center gap-2 text-slate-700">
                    <span className="text-2xl">👾</span> Reddit Discussions
                </h2>
                {redditResults.map((thread, index) => (
                    <div key={index} className="bg-white p-4 rounded-xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
                        <a href={thread.link} target="_blank" rel="noopener noreferrer" className="text-orange-600 font-medium hover:underline block mb-1">
                            {thread.title}
                        </a>
                        <p className="text-sm text-slate-600 line-clamp-2">{thread.snippet}</p>
                    </div>
                ))}
            </motion.div>
        </div>
    );
}
