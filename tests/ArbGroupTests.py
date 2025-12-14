import pytest
from internal_data.ArbGroup import ArbGroup


class TestArbGroupGetSlug:
    """Test cases for ArbGroup.getSlug method"""
    
    def test_get_slug_with_query_parameters(self):
        """Test extracting slug from URL with query parameters"""
        arb_group = ArbGroup([])
        url = "https://polymarket.com/event/will-draftkings-launch-a-prediction-market-in-2025?tid=1765738013669"
        expected_slug = "will-draftkings-launch-a-prediction-market-in-2025"
        
        result = arb_group.getSlug(url)
        assert result == expected_slug
    
    def test_get_slug_without_query_parameters(self):
        """Test extracting slug from URL without query parameters"""
        arb_group = ArbGroup([])
        url = "https://polymarket.com/event/fed-decision-in-january"
        expected_slug = "fed-decision-in-january"
        
        result = arb_group.getSlug(url)
        assert result == expected_slug
    
    def test_get_slug_with_multiple_query_parameters(self):
        """Test extracting slug from URL with multiple query parameters"""
        arb_group = ArbGroup([])
        url = "https://polymarket.com/event/test-slug?tid=123&other=456"
        expected_slug = "test-slug"
        
        result = arb_group.getSlug(url)
        assert result == expected_slug
    
    def test_get_slug_with_trailing_slash(self):
        """Test extracting slug from URL with trailing slash"""
        arb_group = ArbGroup([])
        url = "https://polymarket.com/event/test-slug/"
        expected_slug = "test-slug"
        
        result = arb_group.getSlug(url)
        assert result == expected_slug
    
    def test_get_slug_invalid_url_missing_event(self):
        """Test that ValueError is raised for URL without /event/"""
        arb_group = ArbGroup([])
        url = "https://polymarket.com/some-other-path"
        
        with pytest.raises(ValueError, match="URL is not a Polymarket event URL"):
            arb_group.getSlug(url)
    
    def test_get_slug_invalid_url_wrong_path(self):
        """Test that ValueError is raised for URL with wrong path structure"""
        arb_group = ArbGroup([])
        url = "https://polymarket.com/market/test-slug"
        
        with pytest.raises(ValueError, match="URL is not a Polymarket event URL"):
            arb_group.getSlug(url)
    
    def test_get_slug_with_complex_slug(self):
        """Test extracting slug with hyphens and numbers"""
        arb_group = ArbGroup([])
        url = "https://polymarket.com/event/will-there-be-a-recession-in-2025-2026?tid=999"
        expected_slug = "will-there-be-a-recession-in-2025-2026"
        
        result = arb_group.getSlug(url)
        assert result == expected_slug

