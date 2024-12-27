import os
import uuid
import trimesh
import numpy as np
from xml.etree import ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

class STLto3MFConverter:
    def __init__(self):
        self.namespace = {
            'core': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
        }
        
    def convert(self, stl_path):
        # Load the STL file using trimesh
        mesh = trimesh.load(stl_path)
        
        # Create a temporary directory for the 3MF package
        temp_dir = 'temp'
        os.makedirs(temp_dir, exist_ok=True)
        
        # Generate unique output filename
        output_filename = f"{str(uuid.uuid4())}.3mf"
        output_path = os.path.join(temp_dir, output_filename)
        
        try:
            # Create the 3MF XML structure
            model = self._create_model_xml(mesh)
            model_xml = self._write_model_xml(model)
            
            # Create the 3MF package (ZIP file)
            with ZipFile(output_path, 'w', ZIP_DEFLATED) as zipf:
                # Add the 3D model XML
                zipf.writestr('3D/3dmodel.model', model_xml)
                
                # Add the content types XML
                content_types = self._create_content_types_xml()
                zipf.writestr('[Content_Types].xml', content_types)
                
                # Add the relationships XML
                rels = self._create_relationships_xml()
                zipf.writestr('_rels/.rels', rels)
            
            return output_path
            
        except Exception as e:
            if os.path.exists(output_path):
                os.remove(output_path)
            raise e

    def _create_model_xml(self, mesh):
        # Create the root model element
        ET.register_namespace('', self.namespace['core'])
        model = ET.Element('{%s}model' % self.namespace['core'], {
            'unit': 'millimeter',
            'xml:lang': 'en-US'
        })
        
        # Add resources element
        resources = ET.SubElement(model, '{%s}resources' % self.namespace['core'])
        
        # Add object element
        object_elem = ET.SubElement(resources, '{%s}object' % self.namespace['core'], {
            'id': '1',
            'type': 'model'
        })
        
        # Add mesh element
        mesh_elem = ET.SubElement(object_elem, '{%s}mesh' % self.namespace['core'])
        
        # Add vertices
        vertices_elem = ET.SubElement(mesh_elem, '{%s}vertices' % self.namespace['core'])
        for vertex in mesh.vertices:
            ET.SubElement(vertices_elem, '{%s}vertex' % self.namespace['core'], {
                'x': str(vertex[0]),
                'y': str(vertex[1]),
                'z': str(vertex[2])
            })
        
        # Add triangles
        triangles_elem = ET.SubElement(mesh_elem, '{%s}triangles' % self.namespace['core'])
        for face in mesh.faces:
            ET.SubElement(triangles_elem, '{%s}triangle' % self.namespace['core'], {
                'v1': str(face[0]),
                'v2': str(face[1]),
                'v3': str(face[2])
            })
        
        # Add build element
        build = ET.SubElement(model, '{%s}build' % self.namespace['core'])
        ET.SubElement(build, '{%s}item' % self.namespace['core'], {
            'objectid': '1'
        })
        
        return model

    def _write_model_xml(self, model):
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(model, encoding='unicode', xml_declaration=False)

    def _create_content_types_xml(self):
        types = ET.Element('Types', {
            'xmlns': 'http://schemas.openxmlformats.org/package/2006/content-types'
        })
        
        # Add default content type for rels
        ET.SubElement(types, 'Default', {
            'Extension': 'rels',
            'ContentType': 'application/vnd.openxmlformats-package.relationships+xml'
        })
        
        # Add 3MF model content type
        ET.SubElement(types, 'Override', {
            'PartName': '/3D/3dmodel.model',
            'ContentType': 'application/vnd.ms-package.3dmanufacturing-3dmodel+xml'
        })
        
        return ET.tostring(types, encoding='unicode', xml_declaration=True)

    def _create_relationships_xml(self):
        rels = ET.Element('Relationships', {
            'xmlns': 'http://schemas.openxmlformats.org/package/2006/relationships'
        })
        
        # Add relationship to 3D model
        ET.SubElement(rels, 'Relationship', {
            'Target': '/3D/3dmodel.model',
            'Id': 'rel0',
            'Type': 'http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel'
        })
        
        return ET.tostring(rels, encoding='unicode', xml_declaration=True) 