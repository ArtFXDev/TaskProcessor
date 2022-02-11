//Maya ASCII 2022 scene
//Name: maya_entity_03.ma
//Last modified: Fri, Feb 11, 2022 12:25:14 PM
//Codeset: 1252
requires maya "2022";
requires -nodeType "polyPlatonic" "modelingToolkit" "0.0.0.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2022";
fileInfo "version" "2022";
fileInfo "cutIdentifier" "202102181415-29bfc1879c";
fileInfo "osv" "Windows 10 Home Single Language v2009 (Build: 22000)";
fileInfo "UUID" "5DE359B6-4C8D-9667-BF13-82986AEB56CC";
createNode transform -s -n "persp";
	rename -uid "0CF4852A-4CA9-7685-5DC9-ACB8920B4A4A";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 28 21 28 ;
	setAttr ".r" -type "double3" -27.938352729602379 44.999999999999972 -5.172681101354183e-14 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "4AF47B44-44C8-5334-58CF-21A2E112FBF9";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 44.82186966202994;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "22C3CF4D-43C8-6FCF-7A8B-B0B67B0B0BFD";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "3902C23A-49C8-6BD0-3198-B88F9FC87217";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "16FE1550-4A27-32FF-E468-72A026EC9A9E";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "A5E3FF0A-4EEA-DAA7-9A55-43AD4EC3B26F";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "E8805556-4DD6-49DA-1E6A-699519DC9DF2";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "EEB6F8CF-42F7-CF07-7067-A081A8A87ECB";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "pPlatonic1";
	rename -uid "4A18BBDD-476A-6D1F-235A-929EBA3F0957";
createNode mesh -n "pPlatonicShape1" -p "pPlatonic1";
	rename -uid "00247B1A-4A7D-B01D-2650-ED81086D8E04";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".ndt" 0;
createNode transform -n "RY6F17USWZGM";
	rename -uid "77AD3135-4A1A-B45A-7C77-E89DCF09408F";
createNode mesh -n "RY6F17USWZGMShape" -p "RY6F17USWZGM";
	rename -uid "95415DF8-479A-B4DD-34B7-DE84648EAFA4";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".ndt" 0;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "E44BF7E0-4290-A293-888E-3F996DEC8C48";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "FC857541-463A-8F0F-4763-109D58D04D9A";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "B81D1B1A-410B-A8D8-63C3-4BBC367222E0";
createNode displayLayerManager -n "layerManager";
	rename -uid "0F51154E-44DE-6CD0-BFA0-E9B53B3A94E8";
createNode displayLayer -n "defaultLayer";
	rename -uid "9F622353-4B42-849C-2B19-DD9B7638EDB8";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "F665AFDF-48FA-1A02-71DA-F197922B2F18";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "DDC03A79-4A0E-FB10-88D2-D3B7DFD12493";
	setAttr ".g" yes;
createNode polyPlatonic -n "polyPlatonic1";
	rename -uid "8918FD2F-43AB-610F-ECC5-76B876961B94";
createNode script -n "uiConfigurationScriptNode";
	rename -uid "39EBD9C6-4ED1-39AE-5AD1-FDB2A468781E";
	setAttr ".b" -type "string" "// Maya Mel UI Configuration File.\n// No UI generated in batch mode.\n";
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "CCFE29A2-4DF2-DAE7-E76C-6C8100EDB5D5";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode polySphere -n "polySphere1";
	rename -uid "A3F8BE6E-4F56-AF5C-EA40-A8A949EA6802";
	setAttr ".r" 0.86720415536447382;
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 5 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr -s 2 ".dsm";
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr ".dss" -type "string" "lambert1";
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :defaultColorMgtGlobals;
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "<MAYA_RESOURCES>/OCIO-configs/Maya2022-default/config.ocio";
	setAttr ".wsn" -type "string" "ACEScg";
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "polyPlatonic1.output" "pPlatonicShape1.i";
connectAttr "polySphere1.out" "RY6F17USWZGMShape.i";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "pPlatonicShape1.iog" ":initialShadingGroup.dsm" -na;
connectAttr "RY6F17USWZGMShape.iog" ":initialShadingGroup.dsm" -na;
// End of maya_entity_03.ma
