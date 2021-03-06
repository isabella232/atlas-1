import React, { Component } from "react";

import Content from "../components/Content";
import Layout from "../components/Layout";
import UpdateOfficeForm from "../components/UpdateOfficeForm";

export default class extends Component {
  render() {
    return (
      <Layout>
        <Content>
          <UpdateOfficeForm externalId={this.props.params.externalId} />
        </Content>
      </Layout>
    );
  }
}
