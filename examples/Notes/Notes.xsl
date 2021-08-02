<?xml version="1.0" encoding="UTF-8"?>
<!-- NO BOM !! -->
<xsl:stylesheet version="1.0"
	xmlns="http://www.w3.org/1999/xhtml"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xdh="http://q37.info/ns/xdh">
	<xsl:output method="html" encoding="UTF-8"/>
	<xsl:template match="/XDHTML">
		<xsl:apply-templates select="Notes"/>
	</xsl:template>
	<xsl:template match="Notes">
		<ul>
			<li>
				<span id="View.0"></span>
				<span id="Edit.0"></span>
			</li>
			<xsl:apply-templates select="Note"/>
		</ul>
	</xsl:template>
	<xsl:template match="Note">
		<li>
			<span id="View.{@id}">
				<div>
					<article class="listing note-view" style="width:100%; justify-content: space-between;align-items: center;" xdh:mark="{@id}">
						<div>
							<h3 id="Title.{@id}">
								<xsl:value-of select="title"/>
							</h3>
							<p id="Description.{@id}">
								<!-- 'disable-output-escaping' does not work with Firefox (https://bugzilla.mozilla.org/show_bug.cgi?id=98168)	-->
								<!--xsl:value-of select="description" disable-output-escaping="yes"/-->
							</p>
						</div>
						<span id="Buttons.{@id}" style="flex-direction: row;">
							<button class="button" xdh:onevent="Edit">Edit</button>
							<span style="display:inline-block; width: 10px;"></span>
							<button class="button" xdh:onevent="Delete">Delete</button>
						</span>
					</article>
				</div>
			</span>
			<span id="Edit.{@id}"></span>
		</li>
	</xsl:template>
</xsl:stylesheet>