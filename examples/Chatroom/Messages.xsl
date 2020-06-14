<?xml version="1.0" encoding="UTF-8"?>
<!-- NO BOM !! -->
<xsl:stylesheet version="1.0" xmlns="http://www.w3.org/1999/xhtml" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="html" encoding="UTF-8"/>
	<xsl:template match="/XDHTML">
		<xsl:apply-templates select="Messages"/>
	</xsl:template>
	<xsl:template match="Messages">
		<xsl:apply-templates select="Message"/>
	</xsl:template>
	<xsl:template match="Message">
		<li id="Message.{@id}" data-xdh-value="{@id}">
			<xsl:element name="span">
				<xsl:attribute name="class">
					<xsl:choose>
						<xsl:when test="@pseudo=../@pseudo">
							<xsl:text>self</xsl:text>
						</xsl:when>
						<xsl:otherwise>
							<xsl:text>other</xsl:text>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:attribute>
				<xsl:value-of select="@pseudo"/>
			</xsl:element>
			<xsl:text> : </xsl:text>
			<xsl:value-of select="."/>
		</li>
	</xsl:template>
</xsl:stylesheet>