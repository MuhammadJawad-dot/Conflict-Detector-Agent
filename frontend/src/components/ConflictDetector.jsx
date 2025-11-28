import { motion } from 'framer-motion';

export default function ConflictDetector({ report }) {
    if (!report) return null;

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl shadow-xl border border-slate-100 overflow-hidden"
        >
            <div className="bg-slate-900 text-white p-6">
                <h2 className="text-2xl font-bold flex items-center gap-3">
                    <span>⚖️</span> Conflict Analysis Report
                </h2>
                <p className="text-slate-400 mt-2">{report.final_conflict_report}</p>
            </div>

            <div className="grid md:grid-cols-2 gap-6 p-6">
                {/* Agreements */}
                <div className="space-y-3">
                    <h3 className="font-semibold text-green-600 flex items-center gap-2">
                        <span>✅</span> Agreements
                    </h3>
                    <ul className="space-y-2">
                        {report.agreements.map((item, i) => (
                            <li key={i} className="bg-green-50 text-green-800 px-4 py-2 rounded-lg text-sm border border-green-100">
                                {item}
                            </li>
                        ))}
                    </ul>
                </div>

                {/* Conflicts */}
                <div className="space-y-3">
                    <h3 className="font-semibold text-red-600 flex items-center gap-2">
                        <span>⚠️</span> Conflicts & Disagreements
                    </h3>
                    <ul className="space-y-2">
                        {report.conflicts.map((item, i) => (
                            <li key={i} className="bg-red-50 text-red-800 px-4 py-2 rounded-lg text-sm border border-red-100">
                                {item}
                            </li>
                        ))}
                    </ul>
                </div>

                {/* Unique Insights */}
                <div className="md:col-span-2 grid md:grid-cols-2 gap-6 mt-4 pt-6 border-t border-slate-100">
                    <div>
                        <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-3">Unique to Google</h4>
                        <ul className="space-y-2">
                            {report.unique_google_insights.map((item, i) => (
                                <li key={i} className="text-sm text-slate-600 pl-3 border-l-2 border-blue-200">
                                    {item}
                                </li>
                            ))}
                        </ul>
                    </div>
                    <div>
                        <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-3">Unique to Reddit</h4>
                        <ul className="space-y-2">
                            {report.unique_reddit_insights.map((item, i) => (
                                <li key={i} className="text-sm text-slate-600 pl-3 border-l-2 border-orange-200">
                                    {item}
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
