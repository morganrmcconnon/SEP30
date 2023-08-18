import React, { useState } from 'react';
import VisHeader from './VisHeader';

const TestRoBERTa = () => {
    const [text, setText] = useState("");
    const [resultData, setResultData] = useState({
        sentiment_result: '',
        negative: '',
        neutral: '',
        positive: '',
    });

    const clearText = () => {
        setText("");
        setResultData({
            sentiment_result: '',
            negative: '',
            neutral: '',
            positive: '',
        });
    };

    const getResult = (e) => {
        e.preventDefault();
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 'text': text }),
        };
        fetch("/api/sentiment", requestOptions)
            .then((res) => res.json())
            .then((data) => {
                setResultData({
                    sentiment_result: data['sentiment_result'],
                    negative: data['confidence_probabilities']['negative'],
                    neutral: data['confidence_probabilities']['neutral'],
                    positive: data['confidence_probabilities']['positive'],
                });
            })
            .catch((err) => {
                console.log("Something went wrong NASA!");
                console.error(err);
            });
    };

    return (
        <div className="vis-container">
            <VisHeader title="Test RoBERTa" subtitle="Enter a sentence to check its sentiment" />
            <article>
                <form onSubmit={getResult}>
                    <div>
                        <input
                            type="text"
                            value={text}
                            onChange={(e) => setText(e.target.value)}
                            placeholder="Enter a sentence..."
                        />
                    </div>
                    <div>
                        <button type="submit">Check sentiment</button>
                    </div>
                    <div>
                        <button type="button" onClick={clearText}>Clear</button>
                    </div>
                </form>
                <p>{resultData['sentiment_result']}</p>
                <p>Negative: {resultData['negative']}</p>
                <p>Neutral: {resultData['neutral']}</p>
                <p>Positive: {resultData['positive']}</p>
            </article>
        </div>

    );
};

const TestVader = () => {
    const [text, setText] = useState("");
    const [resultData, setResultData] = useState({
        sentiment_result: '',
        compound_score: '',
    });

    const clearText = () => {
        setText("");
        setResultData({
            sentiment_result: '',
            compound_score: '',
        });
    };

    const getResult = (e) => {
        e.preventDefault();
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 'text': text }),
        };
        fetch("/api/sentiment_vader", requestOptions)
            .then((res) => res.json())
            .then((data) => {
                setResultData({
                    sentiment_result: data['sentiment_label'],
                    compound_score: data['compound_score'],
                });
            })
            .catch((err) => {
                console.log("Something went wrong NASA!");
                console.error(err);
            });
    };

    return (
        <div className="vis-container">
            <VisHeader title="Test Vader" subtitle="Enter a sentence to check its sentiment" />
            <article>
                <form onSubmit={getResult}>
                    <div>
                        <input
                            type="text"
                            value={text}
                            onChange={(e) => setText(e.target.value)}
                            placeholder="Enter a sentence..."
                        />
                    </div>
                    <div>
                        <button type="submit">Check sentiment</button>
                    </div>
                    <div>
                        <button type="button" onClick={clearText}>Clear</button>
                    </div>
                </form>
                <p>{resultData['sentiment_result']}</p>
                <p>Compound Score: {resultData['compound_score']}</p>
            </article>
        </div>

    );
};

export { TestRoBERTa, TestVader };