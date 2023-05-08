import React, { PureComponent } from "react";

/**
 * SearchBar Component
 */
class SearchBar extends PureComponent {
    constructor() {
        super();
        this.state = {
            term: ""
        };
    }

    /**
     * Changes state to match new input
     * @param {*} e onChange event
     */
    onInputChange = e => {
        this.setState({ term: e.target.value});
    };

    /**
     * calls callback function
     * @param {*} e onSubmit event
     */
    onFormSubmit = e => {
        e.preventDefault();
        this.props.onSearchSubmit(this.state.term)
    };

    /**
     * @return {JSX.Element} Search bar and submit button
     */
    render() {
        return (
            <div>
                <form id="searchForm" onSubmit={this.onFormSubmit} className="ui form">
                    <div className="field searchField">
                        <label>Search key terms</label>
                        <input
                            type="text"
                            value={this.state.term}
                            onChange={this.onInputChange}
                        />
                    </div>
                    <p/>
                    <button className="ui button" type="submit">Search</button>
                </form>
            </div>
        );
    }

}

export default SearchBar;
