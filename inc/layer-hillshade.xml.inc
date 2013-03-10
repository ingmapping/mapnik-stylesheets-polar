<Style name="hillshade">
	<Rule>
		<RasterSymbolizer opacity="0.5" scaling="bilinear8" />
	</Rule>
</Style>

<Layer name="hillshade" status="on">
	<StyleName>hillshade</StyleName>
	<Datasource>
		<Parameter name="type">gdal</Parameter>
		<Parameter name="file">hillshade/hillshade.tiff</Parameter>
		<Parameter name="format">tiff</Parameter>
	</Datasource>
</Layer>
