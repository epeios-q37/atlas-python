<?xml version="1.0" encoding="UTF-8"?>
<!-- NO BOM !! -->
<xsl:stylesheet version="1.0"
	xmlns="http://www.w3.org/1999/xhtml"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xdh="http://q37.info/ns/xdh">
	<xsl:output method="html" encoding="UTF-8"/>
	<xsl:template match="/Rooms">
		<fieldset>
			<legend>Rooms</legend>
			<details>
				<summary>Help</summary>
				<fieldset>
				Here are displayed the existing rooms.<br/>Click on a label, or scan the QR Code.
				</fieldset>
			</details>
			<xsl:apply-templates select="Room"/>
		</fieldset>
	</xsl:template>
	<xsl:template match="Room">
		<fieldset style="margin: auto; width: max-content;" xdh:mark="{@id}">
			<legend>
				<a target="_blank" href="{@URL}">
					<xsl:value-of select="."/>
				</a>
			</legend>
			<details xdh:onevent="toggle|QRCode">
				<summary>QR Code</summary>
				<span style="font-style: oblique;">Computing QR Code…</span>
			</details>
		</fieldset>
	</xsl:template>
</xsl:stylesheet>