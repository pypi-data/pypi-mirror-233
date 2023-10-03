import PropTypes from "prop-types";
import React from "react";
import { Grid, Button } from "semantic-ui-react";
import {
  Pagination,
  ResultsMultiLayout,
  ResultsPerPage,
} from "react-searchkit";
import { i18next } from "@translations/oarepo_vocabularies_ui/i18next";
import { ResultCountWithState } from "@js/oarepo_ui";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";

const resultsPerPageLabel = (cmp) => (
  <React.Fragment>
    {cmp} {i18next.t("resultsPerPage")}
  </React.Fragment>
);

export const Results = ({
  sortValues,
  resultsPerPageValues,
  currentResultsState,
  currentFacet,
}) => {
  const { data } = currentResultsState;
  const { total } = data;
  const [[facet, vocabularyItem]] = [...currentFacet];
  const config = React.useContext(SearchConfigurationContext);

  return total ? (
    <React.Fragment>
      <Grid relaxed verticalAlign="middle">
        <Grid.Row width={16}>
          <Grid.Column width={4}>
            <ResultCountWithState />
          </Grid.Column>
          <Grid.Column
            width={4}
            floated="right"
            textAlign="right"
            style={{ marginRight: "0" }}
          >
            <Button
              primary
              fluid
              as="a"
              href={`${config.uiLinks.search}?q=&f=${facet}:${vocabularyItem}`}
              icon="search"
              labelPosition="left"
              content={i18next.t("search")}
              type="button"
            />
          </Grid.Column>
        </Grid.Row>
      </Grid>
      <Grid width={16} textAlign="left" style={{ padding: "2em 0" }}>
        <ResultsMultiLayout />
      </Grid>
      <Grid relaxed verticalAlign="middle" textAlign="center">
        <Grid.Row verticalAlign="middle">
          <Grid.Column className="computer tablet only" width={4}></Grid.Column>
          <Grid.Column
            className="computer tablet only"
            width={8}
            textAlign="center"
          >
            <Pagination
              options={{
                size: "mini",
                showFirst: false,
                showLast: false,
              }}
            />
          </Grid.Column>
          <Grid.Column className="mobile only" width={16} textAlign="center">
            <Pagination
              options={{
                boundaryRangeCount: 0,
                showFirst: false,
                showLast: false,
              }}
            />
          </Grid.Column>
          <Grid.Column
            className="computer tablet only "
            textAlign="right"
            width={4}
          >
            <ResultsPerPage
              values={resultsPerPageValues}
              label={resultsPerPageLabel}
            />
          </Grid.Column>
          <Grid.Column
            className="mobile only mt-10"
            textAlign="center"
            width={16}
          >
            <ResultsPerPage
              values={resultsPerPageValues}
              label={resultsPerPageLabel}
            />
          </Grid.Column>
        </Grid.Row>
      </Grid>
    </React.Fragment>
  ) : null;
};

Results.propTypes = {
  currentResultsState: PropTypes.object.isRequired,
  sortValues: PropTypes.array.isRequired,
  resultsPerPageValues: PropTypes.array.isRequired,
};

Results.defaultProps = {};
