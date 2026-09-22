"""
Crop Maturity Detection Model
Simulates a CNN/Vision-based crop maturity analyzer for harvest readiness.
In production, this would use a fine-tuned EfficientNet or YOLO model trained
on crop maturity datasets. For this demo, it uses deterministic heuristics
seeded by filename/video metadata to produce realistic analysis results.
"""
import os
import json
import random
import hashlib
import math

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(MODEL_DIR), 'data')

# Crop-specific maturity profiles
CROP_MATURITY_PROFILES = {
    'Rice': {
        'days_to_mature': 120,
        'ready_indicators': [
            'Panicles are fully drooping and golden-yellow',
            'Grains are hard and cannot be dented with thumbnail',
            '80-85% of grains on panicle have turned golden',
            'Lower leaves have dried and turned brown'
        ],
        'almost_ready_indicators': [
            'Panicles starting to droop with partial golden color',
            'Grains are firm but still slightly soft',
            '50-70% of grains showing color change',
            'Flag leaf is still green at the tip'
        ],
        'not_ready_indicators': [
            'Panicles are upright and grains are green',
            'Grains are soft and milky when pressed',
            'Most of the plant canopy is still green',
            'Active tillering or flowering still in progress'
        ],
        'color_stages': {'green': 'Vegetative', 'yellow-green': 'Grain filling', 'golden': 'Mature', 'brown': 'Over-mature'},
        'optimal_moisture': '20-22%'
    },
    'Wheat': {
        'days_to_mature': 135,
        'ready_indicators': [
            'Entire spike has turned golden-brown',
            'Grains are hard and break with a snap',
            'Straw has turned completely yellow-brown',
            'Grain moisture content is below 14%'
        ],
        'almost_ready_indicators': [
            'Spike is yellowing but still has green patches',
            'Grains are firm but slightly pliable',
            'Upper internodes have turned yellow',
            'Flag leaf sheath is drying'
        ],
        'not_ready_indicators': [
            'Spike is predominantly green',
            'Grains are soft and doughy',
            'Plant is still actively green',
            'Flowering or grain filling in progress'
        ],
        'color_stages': {'green': 'Vegetative', 'yellow-green': 'Dough stage', 'golden': 'Mature', 'brown': 'Over-mature'},
        'optimal_moisture': '12-14%'
    },
    'Maize': {
        'days_to_mature': 100,
        'ready_indicators': [
            'Husks have turned completely brown and dry',
            'Kernels are firm and glossy with a black layer at base',
            'Silk has turned dark brown/black',
            'Milk line has disappeared — kernel is fully dented'
        ],
        'almost_ready_indicators': [
            'Husks are yellowing and starting to dry',
            'Kernels are firm but milk line still visible',
            'Silk is brown but husk not fully dry',
            'Cob feels firm when squeezed through husk'
        ],
        'not_ready_indicators': [
            'Husks are green and tightly wrapped',
            'Kernels are soft with milky fluid when pressed',
            'Silk is light-colored or just emerging',
            'Plant tassel is still shedding pollen'
        ],
        'color_stages': {'green': 'Vegetative', 'yellow-green': 'Blister/Milk', 'golden': 'Dent/Mature', 'brown': 'Harvest ready'},
        'optimal_moisture': '23-25%'
    },
    'Cotton': {
        'days_to_mature': 160,
        'ready_indicators': [
            'Bolls have fully opened exposing white fluffy lint',
            '60-70% of bolls on the plant are open',
            'Lint is bright white and fully expanded',
            'Boll walls have dried and turned dark brown'
        ],
        'almost_ready_indicators': [
            'Some bolls are cracking open but most are still closed',
            '30-50% of bolls showing signs of opening',
            'Boll walls are browning and hardening',
            'Leaves are starting to shed naturally'
        ],
        'not_ready_indicators': [
            'Bolls are green and tightly closed',
            'Plant is still flowering actively',
            'Squares and young bolls are developing',
            'Canopy is dense green with active growth'
        ],
        'color_stages': {'green': 'Boll development', 'yellow-green': 'Boll maturation', 'white': 'Boll opening', 'brown': 'Fully open'},
        'optimal_moisture': '8-10%'
    },
    'Sugarcane': {
        'days_to_mature': 330,
        'ready_indicators': [
            'Lower leaves have dried and fallen off',
            'Cane juice Brix reading is above 20%',
            'Internodes are fully elongated and hardened',
            'Skin color has changed to yellowish with waxy coating'
        ],
        'almost_ready_indicators': [
            'Lower leaves are yellowing and drying',
            'Internodes are elongated but still slightly soft',
            'Sugar accumulation is progressing (Brix 16-19%)',
            'Growth has slowed significantly'
        ],
        'not_ready_indicators': [
            'Active vegetative growth with green canopy',
            'Internodes are still soft and expanding',
            'Brix reading is below 16%',
            'New leaves and tillers are still emerging'
        ],
        'color_stages': {'green': 'Grand growth', 'yellow-green': 'Ripening', 'golden': 'Mature', 'brown': 'Over-mature'},
        'optimal_moisture': '70-75% (cane)'
    },
    'Tomato': {
        'days_to_mature': 75,
        'ready_indicators': [
            'Fruit is uniformly red/deep red across entire surface',
            'Fruit is firm but gives slightly to gentle pressure',
            'Fruit easily detaches from the vine with light twist',
            'Skin is smooth and glossy with no green patches'
        ],
        'almost_ready_indicators': [
            'Fruit is turning from orange to red (breaker stage)',
            'Some green patches remain near the stem end',
            'Fruit is firm and still attached firmly to vine',
            'Color change is 50-80% complete'
        ],
        'not_ready_indicators': [
            'Fruit is predominantly green',
            'Fruit is hard and small, still sizing up',
            'Flowers or small green fruits visible',
            'Plant is actively growing and flowering'
        ],
        'color_stages': {'green': 'Immature', 'yellow-green': 'Breaker', 'orange': 'Turning', 'red': 'Ripe'},
        'optimal_moisture': 'N/A (pick when ripe)'
    },
    'Banana': {
        'days_to_mature': 120,
        'ready_indicators': [
            'Fingers are plump and rounded (ridges have disappeared)',
            'Skin color has lightened from dark green to light green',
            'Flower remnants at finger tips are dry and easily brushed off',
            'Bunch has been developing for 90-110 days since flowering'
        ],
        'almost_ready_indicators': [
            'Fingers are filling out but slight ridges still present',
            'Skin is medium green with slight color lightening',
            'Bunch size is nearly full but fingers are still angular',
            'Flower remnants are present and starting to dry'
        ],
        'not_ready_indicators': [
            'Fingers are thin and angular with prominent ridges',
            'Skin is dark green',
            'Bunch is small and still developing new hands',
            'Active flowering at the bottom of the bunch'
        ],
        'color_stages': {'dark green': 'Immature', 'green': 'Developing', 'light green': 'Mature (harvest)', 'yellow': 'Ripe (post-harvest)'},
        'optimal_moisture': 'N/A (harvest when mature green)'
    },
    'Mango': {
        'days_to_mature': 130,
        'ready_indicators': [
            'Fruit shoulder has risen above the stem attachment point',
            'Skin color has changed from green to yellow/orange at base',
            'Fruit has a sweet fragrance near the stem end',
            'Fruit gives slightly to gentle squeeze, sap is clear'
        ],
        'almost_ready_indicators': [
            'Fruit has reached full size, shoulder is level with stem',
            'Skin is starting to show yellow tinge at base',
            'Fruit is still firm but not rock-hard',
            'Slight aroma developing'
        ],
        'not_ready_indicators': [
            'Fruit is small and still sizing up',
            'Skin is uniformly dark green',
            'Fruit is very hard with no aroma',
            'Sap is white/milky when stem is cut'
        ],
        'color_stages': {'green': 'Immature', 'yellow-green': 'Mature', 'yellow': 'Ripe', 'orange': 'Fully ripe'},
        'optimal_moisture': 'N/A (pick when mature)'
    },
    'Groundnut': {
        'days_to_mature': 110,
        'ready_indicators': [
            'Inner shell surface has dark brown/black markings',
            'Leaves are yellowing and plants begin to wilt',
            'Pods are firm with dark veining on shell',
            'Kernel fills the entire pod cavity with papery seed coat'
        ],
        'almost_ready_indicators': [
            'Inner shell shows some browning but not fully dark',
            'Lower leaves are yellowing but upper canopy still green',
            'Pods are developing but kernel does not fully fill cavity',
            'Shell veining is visible but not yet dark'
        ],
        'not_ready_indicators': [
            'Plant is fully green with active growth',
            'Pods are soft, white, and watery inside',
            'Flowering and pegging still in progress',
            'Shell has no veining or color markings'
        ],
        'color_stages': {'green': 'Vegetative/Pegging', 'yellow-green': 'Pod filling', 'yellow': 'Maturing', 'brown': 'Ready'},
        'optimal_moisture': '40% (pod)'
    },
    'Onion': {
        'days_to_mature': 120,
        'ready_indicators': [
            '70-80% of tops have fallen over naturally',
            'Neck is thin and starting to dry',
            'Outer scales are papery and dry',
            'Bulb is firm and has reached full size'
        ],
        'almost_ready_indicators': [
            '30-50% of tops are falling over',
            'Neck is softening but still thick',
            'Outer scales are forming but not fully dry',
            'Bulb size is near maximum'
        ],
        'not_ready_indicators': [
            'Tops are upright and green',
            'Active leaf growth continuing',
            'Bulb is small and still expanding',
            'Neck is thick and fleshy'
        ],
        'color_stages': {'green': 'Bulb initiation', 'yellow-green': 'Bulb expansion', 'yellow': 'Maturation', 'brown': 'Cured/Ready'},
        'optimal_moisture': 'Cure until neck is dry'
    }
}


class CropMaturityAnalyzer:
    def __init__(self):
        self.crop_profiles = CROP_MATURITY_PROFILES
        self.supported_crops = list(CROP_MATURITY_PROFILES.keys())

    def extract_colors_from_image(self, image_data, crop_type):
        """Extract dominant colors using OpenCV to determine actual maturity score."""
        try:
            import cv2
            import numpy as np
            
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                return None
                
            # Resize for faster processing
            img = cv2.resize(img, (400, 400))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Color ranges
            lower_red1 = np.array([0, 50, 50])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 50, 50])
            upper_red2 = np.array([180, 255, 255])
            
            lower_green = np.array([35, 40, 40])
            upper_green = np.array([85, 255, 255])
            
            lower_yellow = np.array([11, 40, 40])
            upper_yellow = np.array([34, 255, 255])
            
            mask_red = cv2.bitwise_or(cv2.inRange(hsv, lower_red1, upper_red1), cv2.inRange(hsv, lower_red2, upper_red2))
            mask_green = cv2.inRange(hsv, lower_green, upper_green)
            mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
            
            # Mask out background (too dark or too pale)
            mask_valid = cv2.inRange(hsv, np.array([0, 30, 30]), np.array([180, 255, 255]))
            total = cv2.countNonZero(mask_valid)
            if total == 0: total = 1
            
            red_pct = (cv2.countNonZero(mask_red) / total) * 100
            green_pct = (cv2.countNonZero(mask_green) / total) * 100
            yellow_pct = (cv2.countNonZero(mask_yellow) / total) * 100
            other_pct = max(0, 100 - (red_pct + green_pct + yellow_pct))
            
            # Calculate maturity based on crop
            if crop_type == 'Tomato':
                # Tomato: Red = Ripe (100%), Yellow = Breaker (50%), Green = Immature (10%)
                maturity = (red_pct * 1.1) + (yellow_pct * 0.6) + (green_pct * 0.1)
                golden_pct = yellow_pct
                brown_pct = red_pct
            elif crop_type in ['Banana', 'Mango']:
                # Banana/Mango: Yellow = Ripe (100%), Green = Immature (10%)
                maturity = (yellow_pct * 1.1) + (red_pct * 1.2) + (green_pct * 0.2)
                golden_pct = yellow_pct
                brown_pct = 0
            else:
                # Default for crops like Rice/Wheat: Yellow/Golden = Mature
                maturity = (yellow_pct * 1.1) + (brown_pct * 1.2) + (green_pct * 0.2)
                golden_pct = yellow_pct
                brown_pct = red_pct

            maturity = max(10, min(98, maturity))

            return {
                'maturity_score': maturity,
                'green_pct': green_pct,
                'golden_pct': golden_pct,
                'brown_pct': brown_pct,
                'other_pct': other_pct
            }
        except Exception as e:
            print(f"OpenCV Error: {e}")
            return None

    def analyze_video(self, video_data=None, filename=None, crop_type='Rice'):
        """
        Analyze a crop video for harvest readiness.
        """
        profile = self.crop_profiles.get(crop_type, self.crop_profiles['Rice'])

        seed_str = str(filename or 'sample_video.mp4') + crop_type
        seed_val = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)
        rng = random.Random(seed_val)

        num_frames = rng.randint(8, 12)
        base_maturity = rng.uniform(15, 98)

        frames = []
        for i in range(num_frames):
            timestamp = round((i / (num_frames - 1)) * rng.uniform(8, 30), 1) if num_frames > 1 else 0
            frame_maturity = max(0, min(100, base_maturity + rng.uniform(-12, 12)))

            green_pct = max(5, 100 - frame_maturity + rng.uniform(-8, 8))
            golden_pct = max(5, frame_maturity - 10 + rng.uniform(-5, 5))
            brown_pct = max(0, frame_maturity - 60 + rng.uniform(-5, 5))

            if frame_maturity >= 85: stage, color_dominant = 'Mature', 'red' if crop_type == 'Tomato' else 'golden'
            elif frame_maturity >= 60: stage, color_dominant = 'Maturing', 'yellow-green'
            elif frame_maturity >= 35: stage, color_dominant = 'Developing', 'green'
            else: stage, color_dominant = 'Immature', 'dark green'

            total = green_pct + golden_pct + brown_pct
            frames.append({
                'frame_number': i + 1,
                'timestamp_sec': timestamp,
                'maturity_score': round(frame_maturity, 1),
                'stage': stage,
                'dominant_color': color_dominant,
                'color_distribution': {
                    'green': round(green_pct / total * 100, 1),
                    'golden_yellow': round(golden_pct / total * 100, 1),
                    'brown': round(brown_pct / total * 100, 1),
                    'other': 0.1
                }
            })

        overall_maturity = round(sum(f['maturity_score'] for f in frames) / len(frames), 1)
        return self._build_result(crop_type, overall_maturity, frames, profile, rng, num_frames)

    def analyze_image(self, image_data=None, filename=None, crop_type='Rice'):
        """
        Analyze a single crop image for maturity using actual image pixels.
        """
        profile = self.crop_profiles.get(crop_type, self.crop_profiles['Rice'])
        
        # Generate random generator for remaining fields
        seed_str = str(filename or 'sample_img.jpg') + crop_type
        seed_val = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)
        rng = random.Random(seed_val)

        # Extract actual colors if image data is present
        color_data = None
        if image_data:
            color_data = self.extract_colors_from_image(image_data, crop_type)

        if color_data:
            base_maturity = color_data['maturity_score']
            green_pct = color_data['green_pct']
            golden_pct = color_data['golden_pct']
            brown_pct = color_data['brown_pct']
            other_pct = color_data['other_pct']
        else:
            base_maturity = rng.uniform(15, 98)
            green_pct = max(5, 100 - base_maturity)
            golden_pct = max(5, base_maturity - 10)
            brown_pct = max(0, base_maturity - 60)
            other_pct = 5.0

        if base_maturity >= 85: stage, color_dominant = 'Mature', 'red' if crop_type == 'Tomato' else 'golden'
        elif base_maturity >= 60: stage, color_dominant = 'Maturing', 'yellow-green'
        elif base_maturity >= 35: stage, color_dominant = 'Developing', 'green'
        else: stage, color_dominant = 'Immature', 'dark green'

        total = green_pct + golden_pct + brown_pct + other_pct
        frames = [{
            'frame_number': 1,
            'timestamp_sec': 0.0,
            'maturity_score': round(base_maturity, 1),
            'stage': stage,
            'dominant_color': color_dominant,
            'color_distribution': {
                'green': round(green_pct / total * 100, 1),
                'golden_yellow': round(golden_pct / total * 100, 1),
                'brown': round(brown_pct / total * 100, 1),
                'other': round(other_pct / total * 100, 1)
            }
        }]

        return self._build_result(crop_type, round(base_maturity, 1), frames, profile, rng, 1)

    def _build_result(self, crop_type, overall_maturity, frames, profile, rng, num_frames):
        if overall_maturity >= 80:
            verdict, verdict_code = 'Ready to Harvest', 'ready'
            days_remaining = rng.randint(0, 5)
        elif overall_maturity >= 55:
            verdict, verdict_code = 'Almost Ready', 'almost'
            days_remaining = rng.randint(7, 25)
        else:
            verdict, verdict_code = 'Not Ready Yet', 'not_ready'
            days_remaining = rng.randint(25, int(profile['days_to_mature'] * 0.6))

        if verdict_code == 'ready': indicators = profile['ready_indicators']
        elif verdict_code == 'almost': indicators = profile['almost_ready_indicators']
        else: indicators = profile['not_ready_indicators']

        color_stages = profile.get('color_stages', {})
        maturity_stages = list(color_stages.items())
        if overall_maturity >= 80: current_color_stage = maturity_stages[-1] if maturity_stages else ('golden', 'Mature')
        elif overall_maturity >= 55: current_color_stage = maturity_stages[-2] if len(maturity_stages) >= 2 else maturity_stages[-1]
        elif overall_maturity >= 30: current_color_stage = maturity_stages[1] if len(maturity_stages) >= 2 else maturity_stages[0]
        else: current_color_stage = maturity_stages[0] if maturity_stages else ('green', 'Vegetative')

        confidence = round(rng.uniform(78, 97), 1)

        if verdict_code == 'ready':
            recommendations = [
                f'Harvest within the next {days_remaining} days for optimal quality.',
                f'Ideal crop moisture: {profile["optimal_moisture"]}.',
                'Check weather forecast — avoid harvesting during rain.',
                'Prepare storage and drying facilities in advance.',
                'Use sharp harvesting tools to minimize crop damage.'
            ]
        elif verdict_code == 'almost':
            recommendations = [
                f'Estimated {days_remaining} days until harvest readiness.',
                'Continue monitoring daily for color and firmness changes.',
                f'Target moisture: {profile["optimal_moisture"]}.',
                'Reduce irrigation gradually to encourage maturation.',
                'Begin arranging labor and transport for harvest.'
            ]
        else:
            recommendations = [
                f'Approximately {days_remaining} days remaining until harvest.',
                'Maintain regular irrigation and nutrient schedule.',
                'Monitor for pest and disease pressure during this stage.',
                'Avoid any stress that could delay maturation.',
                'Plan harvesting schedule based on expected maturity date.'
            ]

        return {
            'crop_type': crop_type,
            'verdict': verdict,
            'verdict_code': verdict_code,
            'overall_maturity': overall_maturity,
            'confidence': confidence,
            'days_remaining': days_remaining,
            'current_stage': current_color_stage[1],
            'current_color': current_color_stage[0],
            'indicators': indicators,
            'recommendations': recommendations,
            'optimal_moisture': profile['optimal_moisture'],
            'total_growth_days': profile['days_to_mature'],
            'frames_analyzed': num_frames,
            'frame_analysis': frames,
            'color_stages': color_stages
        }

    def get_supported_crops(self):
        """Return list of supported crop types."""
        return self.supported_crops

    def get_crop_profile(self, crop_type):
        """Return maturity profile for a specific crop."""
        return self.crop_profiles.get(crop_type, None)


if __name__ == '__main__':
    analyzer = CropMaturityAnalyzer()

    # Test analysis
    result = analyzer.analyze_video(filename="test_field_video.mp4", crop_type="Rice")
    print(f"Crop: {result['crop_type']}")
    print(f"Verdict: {result['verdict']}")
    print(f"Maturity: {result['overall_maturity']}%")
    print(f"Confidence: {result['confidence']}%")
    print(f"Days Remaining: {result['days_remaining']}")
    print(f"Current Stage: {result['current_stage']}")
    print(f"\nIndicators:")
    for ind in result['indicators']:
        print(f"  • {ind}")
    print(f"\nFrame Analysis ({result['frames_analyzed']} frames):")
    for frame in result['frame_analysis']:
        print(f"  Frame {frame['frame_number']} @ {frame['timestamp_sec']}s — {frame['stage']} ({frame['maturity_score']}%)")
