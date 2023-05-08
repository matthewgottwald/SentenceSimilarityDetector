import React, { PureComponent } from "react";
import Header from "./Header";
import SearchBar from "./SearchBar";
import UploadFiles from "./UploadFiles";
import Table from "./Table.js";
import axios from "axios";
// const axios = require("axios");

/**
 * Used to determine if the cluster should be in the search results for term
 * @param {string} term
 * @param {list} cluster list of objects that represent rows with {"sentence": string, "file": string}
 * @return {boolean} true if term is a substring of a sentence or fie in cluster, false otherwise
 */
const termInCluster = (term, cluster) => {
  for (let i = 0; i < cluster.length; i++) {
    const row = cluster[i];
    if (
      row["sentence"].toLowerCase().trim().includes(term) ||
      row["file"].toLowerCase().trim().includes(term)
    ) {
      return true;
    }
  }
  return false;
};

/**
 * App Component
 */
class App extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      filenames: [],
      clusters: {},
      searchTerm: "",
    };
  }

  /**
   * Makes post request to backend with the filenames to be compared.
   * Saves results to state
   * @param {list} filenames list of strings
   * @param {Integer} min_samples
   * @param {Number} epsilon
   */
  onFilesSubmit = (filenames, min_samples, epsilon) => {
    this.setState({ filenames });
    axios
      .post("http://127.0.0.1:5000/find_clusters", {
        filenames: filenames,
        min_samples: min_samples,
        epsilon: epsilon,
      })
      .then((response) => {
        console.log("response received");
        this.setState({ clusters: response.data });
        console.log(this.state.clusters[0][0]["sentence"]);
      });
  };

  /**
   * callback function for search bar submition
   * @param {string} searchTerm
   */
  onSearchSubmit = (searchTerm) => {
    this.setState({ searchTerm });
  };

  /**
   * Assembles JSX for the cluster tables
   * @return {[JSX.Element]} list of JSX elements, each one is a table for a cluster
   */
  showTable = () => {
    let data = this.state.clusters;
    let clusters = this.state.clusters;
    let keys = Object.keys(clusters);

    const columns = [
      {
        Header: "Sentence",
        accessor: "sentence",
      },

      {
        Header: "Document",
        accessor: "file",
      },
    ];

    var output = [];

    if (keys.length > 0) {
      output.push(<SearchBar onSearchSubmit={this.onSearchSubmit} />);

      // If -1 exists create an Outlier Table
      if (-1 in data) {
        for (let i = 0; i < keys.length - 1; ++i) {
          if (termInCluster(this.state.searchTerm, data[i])) {
            output.push(
              <div>
                <h3 id="cluster"> Cluster {i}</h3>
                <Table columns={columns} data={data[i]} />
              </div>
            );
          }
        }

        if (termInCluster(this.state.searchTerm, data[-1])) {
          output.push(
            <div>
              <h3 id="cluster">Outliers</h3>
              <Table columns={columns} data={data[-1]} />
            </div>
          );
        }
        // No outliers so create normal tables
      } else {
        for (let i = 0; i < keys.length; ++i) {
          if (termInCluster(this.state.searchTerm, data[i])) {
            output.push(
              <div>
                <h3 id="cluster"> Cluster {i}</h3>
                <Table columns={columns} data={data[i]} />
              </div>
            );
          }
        }
      }
    }
    return output;
  };

  /**
   * render
   * @return {JSX.Element} All of the compenents together
   */
  render() {
    return (
      <div className="App">
        <Header />
        <UploadFiles onFilesSubmit={this.onFilesSubmit} />
        <div>{this.showTable()}</div>
      </div>
    );
  }
}

export default App;
