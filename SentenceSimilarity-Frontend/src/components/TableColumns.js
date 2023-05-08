import { PureComponent } from "react";

class TableColumns extends PureComponent {
  render() {
    const headers = [
      {
        Header: "Sentence",
        accessor: "sentence",
      },

      {
        Header: "Document",
        accessor: "file",
      },
    ];
    return headers;
  }
}

export default TableColumns;
