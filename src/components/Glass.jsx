import "./Glass.css";
import { useState } from "react";
import axios from "axios";

function Glass() {
  const [path, setPath] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
    const params = { path };
    console.log(params);

    axios
      .post("http://localhost:8080/predict", params)
      .then((res) => {
        const data = res.data.message;
        alert(data);
        reset();
      })
      .catch((error) => alert(`Error: ${error.message}`));
  };

  const reset = () => {
    setPath("");
    setSubmitted(false);
  };

  return (
    <div className="glass">
      {/* <form action="http://localhost:8080/uploadfile" enctype="multipart/form-data" method="post">
        <input name="files" type="file" />
        <button type="submit" />
      </form> */}
      <form onSubmit={(e) => handleSubmit(e)} className="glass__form">
        <h4>Music Path</h4>
        <div className="glass__form__group">
          <input
            id="path"
            className="glass__form__input"
            placeholder="Music Path"
            required
            autoFocus
            title="Music Path"
            type="string"
            value={path}
            onChange={(e) => setPath(e.target.value)}
          />
        </div>

        <div className="glass__form__group">
          {submitted && <p>Submitted. Please wait.</p>}
          {!submitted && (
            <button type="submit" className="glass__form__btn">
              Submit
            </button>
          )}
        </div>
      </form>
    </div>
  );
}

export default Glass;
