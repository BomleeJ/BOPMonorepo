import pytest
from internal_data.ArbGroup import ArbGroup, ArbGroupFactory


class TestArbGroupGetSlug:
    """Test cases for ArbGroup.getSlug method"""
    
    def test_get_slug_without_query_parameters(self):
        """Test extracting slug from URL without query parameters"""
        factory = ArbGroupFactory("https://polymarket.com/event/test")
        url = "https://polymarket.com/event/fed-decision-in-january"
        expected_slug = "fed-decision-in-january"
        
        result = factory.getSlug(url)
        assert result == expected_slug
    
    def test_get_slug_with_multiple_query_parameters(self):
        """Test extracting slug from URL with multiple query parameters"""
        factory = ArbGroupFactory("https://polymarket.com/event/test")
        url = "https://polymarket.com/event/test-slug?tid=123&other=456"
        expected_slug = "test-slug"
        
        result = factory.getSlug(url)
        assert result == expected_slug
    
    def test_get_slug_with_trailing_slash(self):
        """Test extracting slug from URL with trailing slash"""
        factory = ArbGroupFactory("https://polymarket.com/event/test")
        url = "https://polymarket.com/event/test-slug/"
        expected_slug = "test-slug"
        
        result = factory.getSlug(url)
        assert result == expected_slug
    
    def test_get_slug_invalid_url_missing_event(self):
        """Test that ValueError is raised for URL without /event/"""
        factory = ArbGroupFactory("https://polymarket.com/event/test")
        url = "https://polymarket.com/some-other-path"
        
        with pytest.raises(ValueError, match="URL is not a Polymarket event URL"):
            factory.getSlug(url)
    
    def test_get_slug_invalid_url_wrong_path(self):
        """Test that ValueError is raised for URL with wrong path structure"""
        factory = ArbGroupFactory("https://polymarket.com/event/test")
        url = "https://polymarket.com/market/test-slug"
        
        with pytest.raises(ValueError, match="URL is not a Polymarket event URL"):
            factory.getSlug(url)
    
    def test_get_slug_with_complex_slug(self):
        """Test extracting slug with hyphens and numbers"""
        factory = ArbGroupFactory("https://polymarket.com/event/test")
        url = "https://polymarket.com/event/will-there-be-a-recession-in-2025-2026?tid=999"
        expected_slug = "will-there-be-a-recession-in-2025-2026"
        
        result = factory.getSlug(url)
        assert result == expected_slug


class TestArbGroupInitialization:
    """Test cases for ArbGroup initialization with real URLs"""
    
    # URL strings
    democratic_nominee_2028_url = "https://polymarket.com/event/democratic-presidential-nominee-2028"
    fed_decision_january_url = "https://polymarket.com/event/fed-decision-in-january?tid=1765731059021"
    draftkings_prediction_market_url = "https://polymarket.com/event/will-draftkings-launch-a-prediction-market-in-2025?tid=1765745562883"

    # Sets
    rate_change_outcomes = {
        "50+ bps decrease",
        "25 bps decrease",
        "No change"
    }

    democratic_candidates = {
        "Gavin Newsom",
        "Josh Shapiro",
        "Pete Buttigieg"
    }

    def testWithoutGroupItems(self):
        
        a = ArbGroup("https://polymarket.com/event/will-draftkings-launch-a-prediction-market-in-2025?tid=1765745562883", "https://polymarket.com/event/democratic-presidential-nominee-2028", None, None)

        print(a)
        assert True
    

