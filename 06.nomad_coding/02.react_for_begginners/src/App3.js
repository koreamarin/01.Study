import { useEffect, useState } from "react";

function App3() {
  const [loading, setLoading] = useState(true);
  const [coins, setCoins] = useState([]);
  useEffect(() => {
    fetch("https://api.coinpaprika.com/v1/tickers")
        .then(response => response.json())
        .then(json => {
            setCoins(json);
            setLoading(false);
        });
    }, [])

  return (
    <div>
      <h1>The Coins! {loading ? null : `(${coins.length})`}</h1>
        {loading ? <strong>Loding...</strong> : null}
        <select>
            {coins.map((coin) => (
                <option key={coin.id}>
                    {coin.name} ({coin.symbol})
                    ${Math.round(coin.quotes.USD.price)} USD
                </option>
            ))}
        </select>
    </div>
    );
    
}

export default App3;
