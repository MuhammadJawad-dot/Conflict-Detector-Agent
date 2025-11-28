import { useState } from 'react';
import Hero from '../components/Hero';
import SearchInput from '../components/SearchInput';
import Results from '../components/Results';
import ConflictDetector from '../components/ConflictDetector';
import { searchGoogle, searchReddit, analyzeConflicts } from '../services/api';

export default function Home() {
    const [isLoading, setIsLoading] = useState(false);
    const [googleResults, setGoogleResults] = useState([]);
    const [redditResults, setRedditResults] = useState([]);
    const [conflictReport, setConflictReport] = useState(null);
    const [error, setError] = useState(null);

    const handleSearch = async (query) => {
        setIsLoading(true);
        setError(null);
        setGoogleResults([]);
        setRedditResults([]);
        setConflictReport(null);

        try {
            // 1. Parallel Search
            const [googleRes, redditRes] = await Promise.all([
                searchGoogle(query),
                searchReddit(query)
            ]);

            setGoogleResults(googleRes);
            setRedditResults(redditRes.threads); // Display threads

            // 2. Analyze Conflicts
            // We pass the scraped content from Reddit (redditRes.content)
            const report = await analyzeConflicts(googleRes, redditRes.content);
            setConflictReport(report);

        } catch (err) {
            console.error(err);
            setError("Failed to fetch results. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-slate-50 px-4 pb-20">
            <div className="max-w-6xl mx-auto">
                <Hero />

                <SearchInput onSearch={handleSearch} isLoading={isLoading} />

                {error && (
                    <div className="text-center text-red-500 mb-8 p-4 bg-red-50 rounded-lg">
                        {error}
                    </div>
                )}

                {isLoading && (
                    <div className="flex justify-center my-12">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
                    </div>
                )}

                {(googleResults.length > 0 || redditResults.length > 0) && (
                    <>
                        <Results googleResults={googleResults} redditResults={redditResults} />
                        <ConflictDetector report={conflictReport} />
                    </>
                )}
            </div>
        </div>
    );
}
