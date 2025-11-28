import { motion } from 'framer-motion';

export default function Hero() {
    return (
        <div className="text-center py-12">
            <motion.h1
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent mb-4"
            >
                Conflict Detector Agent
            </motion.h1>
            <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
                className="text-slate-500 text-lg"
            >
                Compare Official Sources vs. Community Wisdom
            </motion.p>
        </div>
    );
}
