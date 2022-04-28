/* eslint-disable jsx-a11y/anchor-is-valid */
import { useState } from "react";
import "./App.css";
import axios from "axios";

function App() {
  // states
  const [text, setText] = useState("");
  const [threshold, setThreshold] = useState(0.45);
  const [n, setN] = useState(1);
  const [outSummary, setOutSummary] = useState("")
  const [pointSummary, setPointSummary] = useState("")
  const [nSentSummary, setNSentSummary] = useState("")

  window.onscroll = function(){
    document.getElementById("theta").style.bottom="15%";
    document.getElementById("theta").style.left="2%";
  }

  // functions
  const findSummary = () => {
    setOutSummary("")
    axios
      .post("http://localhost:5000/abstract", {
        text: text,
        threshold: threshold,
      })
      .then((res) => {
        const received_summary = res.data.summary
        console.log(received_summary)
        let s = ""
        received_summary.forEach(element => {
          s+=element+'\n'
          console.log(s)
        });
        setOutSummary(s)
      });
  };

  const findPointwiseSummary = () => {
    setPointSummary("")
    axios
      .post("http://localhost:5000/pointwise", {
        text: text,
        threshold: threshold,
      })
      .then((res) => {
        const received_summary = res.data.summary
        console.log(received_summary)
        let s = ''
        received_summary.forEach(element => {
          s+='• '+element+'\n'
        });
        setPointSummary(s)
      });
  };

  const findNSents = () => {
    setNSentSummary("")
    axios
      .post("http://localhost:5000/topnsent", {
        text: text,
        threshold: threshold,
        n: n,
      })
      .then((res) => {
        const received_summary = res.data.summary
        console.log(received_summary)
        let s = ''
        received_summary.forEach(element => {
          s+='• '
          element.forEach(item => {
            s+=item+'\n'
          })
          s+='\n'
        });
        setNSentSummary(s)
      });
  };

  return (
    <>
      <nav className="navbar fixed-top navbar-expand-lg navbar-dark">
        <div className="container-fluid">
          <a className="navbar-brand " href="#">
            <img src="Logo.png" alt="GistIt!" height="60px" />
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
              <li className="nav-item mx-5">
                <a
                  className="nav-link active"
                  aria-current="page"
                  href="#inputtext"
                >
                  Home
                </a>
              </li>
              <li className="nav-item mx-5">
                <a
                  className="nav-link active"
                  aria-current="page"
                  href="#abssum"
                >
                  Summarize
                </a>
              </li>
              <li className="nav-item mx-5">
                <a
                  className="nav-link active"
                  aria-current="page"
                  href="#pointsum"
                >
                  Pointwise Summary
                </a>
              </li>
              <li className="nav-item mx-5">
                <a
                  className="nav-link active"
                  aria-current="page"
                  href="#numsum"
                >
                  Important Sentences
                </a>
              </li>
              <li className="nav-item mx-5">
                <a
                  className="nav-link active"
                  aria-current="page"
                  href="#howto"
                >
                  How to Use
                </a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      <div className="gap-custom"></div>

      <div className="container main-body">
        <div className="row gx-5" id="inputtext">
          <div className="col-md-5 col-sm-12 mb-5 textpane">
            <div>
              <h3>Process in text to produce:</h3>
              <ul>
                <li>Summary</li>
                <li>Pointwise Summary</li>
                <li>Find Important Sentences</li>
              </ul>
              <h4>In just ONE click!</h4>
              <h5>
                Also, use the slider to go deeper or shallower into your
                Summary!
              </h5>
            </div>
            <div className="forslider1" id="theta">
              <div className="slider1">
                <label htmlFor="threshold" className="form-label">
                  {" "}
                  &#62;&#62; Dive Deeper &#62;&#62;
                </label>
                <input
                  type="range"
                  className="form-range"
                  id="threshold"
                  min="0.20"
                  max="0.90"
                  value={threshold}
                  step="0.01"
                  onChange={(e) => setThreshold(parseFloat(e.target.value))}
                />
              </div>
            </div>
          </div>
          <div className="col-md-7 col-sm-12 mb-5">
            <div className="container gistit-panes input-group">
              <textarea
                placeholder="Type here..."
                className="form-control"
                aria-label="Input Text"
                id="raw-text"
                name="raw-text"
                onChange={(e) => setText(e.target.value)}
              />
            </div>
          </div>
        </div>

        <div className="row gx-5" id="abssum">
          <div className="col-md-7 col-sm-12 mb-5">
            <div className="container gistit-panes input-group">
              <textarea
                placeholder="Summary"
                className="form-control"
                aria-label="Abstract Summary"
                id="abs-sum"
                name="abs-sum"
                value={outSummary}
              />
            </div>
          </div>
          <div className="col-md-5 col-sm-12 mb-5 textpane">
            Use the "Get Summary" button to get an adjective summary.
            <br />
            Also, don't forget to use the slider to specify the depth of summary
            you want!
            <br />
            <br />
            <br />
            <br />
            <div className="pushtocenter">
              <button
                id="getsummary"
                className="gistbuttons"
                onClick={findSummary}
              >
                Get Summary
              </button>
            </div>
          </div>
        </div>

        <div className="row gx-5" id="pointsum">
          <div className="col-md-5 col-sm-12 mb-5 textpane">
            Use the "Get Points" button to get pointwise summary from the text
            entered.
            <br />
            You can increase or decrease the number of points by using the
            slider again to change the depth of summary.
            <br />
            <br />
            <br />
            <br />
            <div className="pushtocenter">
              <button
                id="getpoints"
                className="gistbuttons"
                onClick={findPointwiseSummary}
              >
                Get Points
              </button>
            </div>
          </div>
          <div className="col-md-7 col-sm-12 mb-5">
            <div className="container gistit-panes input-group">
              <textarea
                placeholder="Points"
                className="form-control"
                aria-label="Pointwise Summary"
                id="pnt-text"
                name="pnt-text"
                value={pointSummary}
              />
            </div>
          </div>
        </div>

        <div className="row gx-5" id="numsum">
          <div className="col-md-7 col-sm-12 mb-5">
            <div className="container gistit-panes input-group">
              <textarea
                placeholder="Important Sentences"
                className="form-control"
                aria-label="Top N SEntences"
                id="num-text"
                name="num-text"
                value={nSentSummary}
              />
            </div>
          </div>
          <div className="col-md-5 col-sm-12 mb-5 textpane">
            Retain 'n' most important from each subtopic.
            <br />
            Enter the the number of sentences you want from each subtopic and
            click on the "Get Important Sentences" button.
            <br />
            Again, you can decide if you want more details, then to use the
            slider.
            <br />
            <br />
            <br />
            <br />
            <div className="input-group mb-3">
              <span className="input-group-text" id="basic-addon3">
                Enter the Value of 'n':
              </span>
              <input
                type="number"
                className="form-control"
                value={n}
                aria-label="nsent"
                aria-describedby="basic-addon1"
                id="nsent"
                min="1"
                onChange={(e) => setN(e.target.value)}
              />
            </div>
            <div className="pushtocenter">
              <button
                id="getsents"
                className="gistbuttons"
                onClick={findNSents}
              >
                Get Important Sentences
              </button>
            </div>
          </div>
        </div>

        <div className="row gx-5" id="howto">
          <div className="col-md-12 col-sm-12 mb-5 textpane">
            <h3>How to Use GistIt!</h3>
            Enter the the text tou want to summarize in the first or topmost
            pane.
            <br />
            To get the topicwise summary, you can scroll a bit down, near the
            second pane, to click the "Get Summary" button. The summary will be
            shown the second pane.
            <br />
            To get the pointwise summary, scroll a bit further and click the
            "Get Points" button. The points will be displayed in the third pane.
            <br />
            To get the most 'n' important sentences, type the number in the
            textfield near the last pane and click on "Get Importanat Sentences"
            button. The sentences will be displayed in the last pane.
            <br />
            Important Note: For each of above three functionalities, you can use
            the slider and click on the respective buttons again to increase or
            decrease the depth of the summary.
          </div>
        </div>
      </div>

      <footer className="gistitfooter">
        <div className="text-center p-4">
          © 2022 Copyright: Anwesha and Kritika
        </div>
      </footer>
    </>
  );
}

export default App;
