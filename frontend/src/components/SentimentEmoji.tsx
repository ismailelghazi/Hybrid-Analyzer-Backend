import './SentimentEmoji.css';

interface SentimentEmojiProps {
    sentiment: 'positif' | 'negatif' | 'neutre' | string;
    size?: 'sm' | 'md' | 'lg';
    showLabel?: boolean;
}

export const SentimentEmoji = ({
    sentiment,
    size = 'md',
}: SentimentEmojiProps) => {
    const getSentimentData = () => {
        const normalizedSentiment = sentiment.toLowerCase();

        switch (normalizedSentiment) {
            case 'positif':
            case 'positive':
                return {
                    label: 'Positive',
                    colorClass: 'sentiment--positive',
                };
            case 'negatif':
            case 'negative':
                return {
                    label: 'Negative',
                    colorClass: 'sentiment--negative',
                };
            case 'neutre':
            case 'neutral':
            default:
                return {
                    label: 'Neutral',
                    colorClass: 'sentiment--neutral',
                };
        }
    };

    const { label, colorClass } = getSentimentData();

    return (
        <div className={`sentiment sentiment--${size} ${colorClass}`}>
            <span className="sentiment__label">{label}</span>
        </div>
    );
};

export default SentimentEmoji;


