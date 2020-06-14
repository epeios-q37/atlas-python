<?xml version="1.0" encoding="UTF-8"?>
<!-- NO BOM !! -->
<xsl:stylesheet version="1.0" 
	xmlns="http://www.w3.org/1999/xhtml" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="html" encoding="UTF-8"/>
	<xsl:template match="/Board">
		<table>
			<tbody>
				<xsl:apply-templates select="Row"/>
			</tbody>
		</table>
	</xsl:template>
	<xsl:template match="Row">
		<tr>
			<xsl:apply-templates select="Square"/>
		</tr>
	</xsl:template>
	<xsl:template match="Square">
		<td id="{@x}{../@y}">
			<xsl:if test="@Playable='true'">
				<xsl:attribute name="data-xdh-onevent">Play</xsl:attribute>
			</xsl:if>
			<xsl:attribute name="class">
				<xsl:choose>
					<xsl:when test=".='Dark'">
						<xsl:text>black</xsl:text>
					</xsl:when>
					<xsl:when test=".='Light'">
						<xsl:text>white</xsl:text>
					</xsl:when>
					<xsl:otherwise>
						<xsl:text>none</xsl:text>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:attribute>
		</td>
	</xsl:template>
</xsl:stylesheet>