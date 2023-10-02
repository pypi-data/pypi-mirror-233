import json
import os
import unittest
import drb.topics.resolver as resolver
from drb.core.node import DrbNode
from drb.metadata import MetadataAddon


class TestSentinel2Metadata(unittest.TestCase):
    md_resolver: MetadataAddon = None
    data_dir: str = None
    expected: dict = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.md_resolver = MetadataAddon()
        cls.data_dir = os.path.join(os.path.dirname(__file__), 'resources')
        with open(os.path.join(cls.data_dir, 'expected.json')) as file:
            cls.expected = json.load(file)

    def _check_metadata(self, expected: dict, node: DrbNode) -> tuple:
        """
        Checks if the given node have all expected metadata and checks also
        their values.

        Parameters:
            expected (dict):
            node (DrbNode):
        Returns:
             tuple(bool, dict): True and an empty dict if all actual metadata
                                are equal to expected metadata, otherwise False
                                and a diff report dict.
        """
        metadata = self.md_resolver.apply(node)
        report = {}
        for key, value in expected.items():
            if key not in metadata.keys():
                report[key] = 'metadata missing'
                continue
            actual = metadata[key]
            if value != actual:
                report[key] = {'expected': value, 'actual': actual}

        return len(report) == 0, report

    def test_sentinel2_level2A_product_metadata(self):
        product = "S2A_MSIL2A_20220718T061641_N0400_" \
                  "R034_T42TVL_20220718T101253.SAFE"
        node = resolver.resolve(os.path.join(self.data_dir, product))
        self.assertEqual('Sentinel-2 User Product Level-2A', node[0].label)
        rc, report = self._check_metadata(self.expected[node[1].name], node[1])
        self.assertTrue(rc, report)

    def test_sentinel2_level1C_product_metadata(self):
        product = "S2B_MSIL1C_20220720T092559_N0400_" \
                  "R136_T34SEH_20220720T101237.SAFE"
        node = resolver.resolve(os.path.join(self.data_dir, product))
        self.assertEqual('Sentinel-2 User Product Level-1C', node[0].label)
        rc, report = self._check_metadata(self.expected[node[1].name], node[1])
        self.assertTrue(rc, report)

    def test_sentinel2_DS_level0_product_metadata_tar(self):
        product = "S2B_OPER_MSI_L0__DS_SGS__20191014T075559" \
                  "_S20191014T050726_N02.08.tar"
        node = resolver.resolve(os.path.join(self.data_dir, product))
        self.assertEqual('Sentinel-2 Level-0 Datastrip tar', node[0].label)
        rc, report = self._check_metadata(self.expected[node[1].name], node[1])
        self.assertTrue(rc, report)

    def test_sentinel2_DS_level0_product_metadata(self):
        product = "S2B_OPER_MSI_L0__DS_SGS__20191014T075559" \
                  "_S20191014T050726_N02.08"
        node = resolver.resolve(os.path.join(self.data_dir, product))
        self.assertEqual('Sentinel-2 Level-0 Datastrip', node[0].label)
        rc, report = self._check_metadata(self.expected[node[1].name], node[1])
        self.assertTrue(rc, report)

    def test_sentinel2_GR_level0_product_metadata_tar(self):
        product = "S2A_OPER_MSI_L0__GR_SGS__20191001T101733" \
                  "_S20191001T083650_D01_N02.08.tar"
        node = resolver.resolve(os.path.join(self.data_dir, product))
        self.assertEqual('Sentinel-2 Level-0 Granule tar', node[0].label)
        rc, report = self._check_metadata(self.expected[node[1].name], node[1])
        self.assertTrue(rc, report)

    def test_sentinel2_GR_level0_product_metadata(self):
        product = "S2A_OPER_MSI_L0__GR_SGS__20191001T101733" \
                  "_S20191001T083650_D01_N02.08"
        node = resolver.resolve(os.path.join(self.data_dir, product))
        self.assertEqual('Sentinel-2 Level-0 Granule', node[0].label)
        rc, report = self._check_metadata(self.expected[node[1].name], node[1])
        self.assertTrue(rc, report)

    def test_sentinel2_HKTM_product_metadata_tar(self):
        product = "S2A_OPER_PRD_HKTM___20191203T051837" \
                  "_20191203T051842_0001.tar"
        node = resolver.resolve(os.path.join(self.data_dir, product))
        self.assertEqual('Sentinel-2 Level-0 HKTM', node[0].label)
        rc, report = self._check_metadata(self.expected[node[1].name], node[1])
        self.assertTrue(rc, report)

    def test_sentinel2_SAD_product_metadata_tar(self):
        product = "S2A_OPER_AUX_SADATA_EPAE_20190222T003515" \
                  "_V20190221T190438_20190221T204519_A019158_WF_LN.tar"
        node = resolver.resolve(os.path.join(self.data_dir, product))
        self.assertEqual('Sentinel-2 Auxiliary SAD PDI', node[0].label)
        rc, report = self._check_metadata(self.expected[node[1].name], node[1])
        self.assertTrue(rc, report)

    def test_sentinel2_L1C_TCI_product_metadata_tar(self):
        product = "S2B_OPER_MSI_L1C_TC_MTI__20140630T140000" \
                  "_A015533_T41UMR_N01.01.tar"
        node = resolver.resolve(os.path.join(self.data_dir, product))
        self.assertEqual('Sentinel-2 Level-1C Tile Image File', node[0].label)
        rc, report = self._check_metadata(self.expected[node[1].name], node[1])
        self.assertTrue(rc, report)

    def test_sentinel2_GIPP_AUX_product_metadata_tar(self):
        product = "S2B_OPER_GIP_G2PARA_MPC__20170206T103032" \
                  "_V20170101T000000_21000101T000000_B00.TGZ"
        node = resolver.resolve(os.path.join(self.data_dir, product))
        self.assertEqual('Sentinel-2 Auxiliary GIP', node[0].label)
        rc, report = self._check_metadata(self.expected[node[1].name], node[1])
        self.assertTrue(rc, report)

    def test_sentinel2_ECMWFD_UT1UTC_AUX_product_metadata_tar(self):
        product = "S2__OPER_AUX_ECMWFD_PDMC_20190216T120000" \
                  "_V20190217T090000_20190217T210000.TGZ"
        node = resolver.resolve(os.path.join(self.data_dir, product))
        self.assertEqual('Sentinel-2 Auxiliary ECMWFD', node[0].label)
        rc, report = self._check_metadata(self.expected[node[1].name], node[1])
        self.assertTrue(rc, report)

    def test_sentinel2_EOF_AUX_product_metadata(self):
        product = "S2A_OPER_AUX_RESORB_OPOD_20181113T031139" \
                  "_V20181112T211554_20181113T003924.EOF"
        node = resolver.resolve(os.path.join(self.data_dir, product))
        self.assertEqual('Sentinel-2 EOF Restituted Orbit'
                         ' File Auxiliary Product', node[0].label)
        rc, report = self._check_metadata(self.expected[node[1].name], node[1])
        self.assertTrue(rc, report)
