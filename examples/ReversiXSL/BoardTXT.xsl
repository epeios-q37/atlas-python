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
			<xsl:choose>
				<xsl:when test=".='Dark'">
					<xsl:text>X</xsl:text>
				</xsl:when>
				<xsl:when test=".='Light'">
					<xsl:text>O</xsl:text>
				</xsl:when>
				<xsl:otherwise>
					<xsl:if test="@Playable='true'">
						<xsl:attribute name="data-xdh-onevent">Play</xsl:attribute>
					</xsl:if>
				</xsl:otherwise>
			</xsl:choose>
		</td>
	</xsl:template>
</xsl:stylesheet>