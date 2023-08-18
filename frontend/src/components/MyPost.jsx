import React, { useState } from 'react';
import VisHeader from './VisHeader';

const MyPost = () => {
    const [text, setText] = useState("");
    const [resultText, setResultText] = useState("");

    const clearText = () => {
        setText("");
        setResultText("");
    };

    const getResult = (e) => {
        e.preventDefault();
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text }),
        };
        fetch("/api/sentiment", requestOptions)
            .then((res) => res.json())
            .then((data) => {
                setResultText(data['sentiment_result']);
            })
            .catch((err) => {
                console.log("Something went wrong NASA!");
                console.error(err);
            });
    };

    return (
        <div className="vis-container">
            <VisHeader title="Test Sentiment Analysis" subtitle="Enter a sentence to check its sentiment" />
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
                <p>{resultText}</p>
            </article>
        </div>

    );
};

export default MyPost;