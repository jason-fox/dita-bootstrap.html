<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright © 2017 · infotexture · Roger W. Fienhold Sheen -->
<!-- See the accompanying LICENSE file for applicable license -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="3.0">
  <!--
    For DITA-OT 3.0, 3.1 and 3.2 import a version of the
    HTML transform without reference to Hazard Statements
  -->
  <xsl:import href="plugin:org.dita-bootstrap.html:xsl/dita2html5-legacy-3.0.xsl"/>

  <xsl:output
    method="html"
    include-content-type="no"
    indent="no"
    doctype-system="about:legacy-compat"
    omit-xml-declaration="yes"
  />

  <!-- root rule -->
  <xsl:template match="/">
    <xsl:apply-templates/>
  </xsl:template>
</xsl:stylesheet>
