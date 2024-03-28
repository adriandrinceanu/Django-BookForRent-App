import { useEffect, useState } from "react";

const useBookData = () => {
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);
  
    useEffect(() => {
      fetch("http://127.0.0.1:8000/api/book/") // r
        .then((response) => {
          if (response.status >= 400) {
            throw new Error("server error");
          }
          return response.json();
        })
        .then((response) => setData(response))
        .catch((error) => setError(error))
        .finally(() => setLoading(false));
    }, []);
  
    return { data, error, loading };
  };
  
  const BookList = () => {
    const { data, error, loading } = useBookData();
  
    if (error) return <p>A network error was encountered</p>;
    if (loading) return <p>Loading...</p>;
  
    return (
      <div className="row row-cols-1 row-cols-sm-2 row-cols-md-5 g-4">
        {data.map((book, index) => (
          <div className="col" key={index}>
            <div className="card shadow-sm">
              <img src={book.image} className="bd-placeholder-img card-img-top" width="100%" height="300" alt={book.title} />
              <div className="card-body">
                <h5 className="card-title">{book.title}</h5>
                <p className="card-text">Author: {book.author}</p>
                <hr />
                <p>Genre: {book.genres.join(", ")}</p>
                <hr />
                <p>Rating: {book.rating}</p>
                <div className="d-flex justify-content-between align-items-center">
                  <div className="btn-group">
                    <button className="btn btn-sm btn-outline-secondary">View</button>
                    <button className="btn btn-sm btn-outline-primary">Rent</button>
                  </div>
                  <small className="text-body-secondary">{book.quantity} books left</small>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  };


export default BookList;