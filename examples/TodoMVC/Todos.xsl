<?xml version="1.0" encoding="UTF-8"?>
<!-- NO BOM !! -->
<xsl:stylesheet version="1.0"
	xmlns="http://www.w3.org/1999/xhtml"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xdh="http://q37.info/ns/xdh">
	<xsl:output method="html" encoding="UTF-8"/>
	<xsl:template match="/XDHTML">
		<xsl:apply-templates select="Todos"/>
	</xsl:template>
	<xsl:template match="Todos">
		<xsl:apply-templates select="Todo"/>
	</xsl:template>
	<xsl:template match="Todo">
		<li id="Todo.{@id}" xdh:onevents="(dblclick|Edit)" xdh:mark="{@id}">
			<xsl:attribute name="class">
				<xsl:text>view</xsl:text>
				<xsl:choose>
					<xsl:when test="@completed='true'">
						<xsl:text> completed</xsl:text>
					</xsl:when>
					<xsl:otherwise>
						<xsl:text> active</xsl:text>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:attribute>
			<span id="View.{@id}">
				<input class="toggle" type="checkbox" id="{@id}" xdh:onevent="Toggle">
					<xsl:if test="@completed='true'">
						<xsl:attribute name="checked"/>
					</xsl:if>
				</input>
				<label id="Label.{@id}">
					<xsl:value-of select="."/>
				</label>
				<button xdh:mark="{@id}" class="destroy" xdh:onevent="Destroy"/>
			</span>
			<input id="Input.{@id}" class="edit" xdh:onevent="Submit" xdh:onevents="(keyup|Cancel|Esc)(blur|Submit)"/>
		</li>
	</xsl:template>
</xsl:stylesheet>