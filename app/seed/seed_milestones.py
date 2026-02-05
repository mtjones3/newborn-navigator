"""
Seed script for newborn milestone data (weeks 0-16).

Run with:
    python -m app.seed.seed_milestones

Sources referenced for clinical accuracy:
    - AAP  (American Academy of Pediatrics)
    - CDC  (Centers for Disease Control and Prevention)
    - WHO  (World Health Organization)
"""

from app.database import Base, engine, SessionLocal
from app.models.milestone import Milestone


# ---------------------------------------------------------------------------
# Milestone data
# ---------------------------------------------------------------------------

MILESTONES = [
    # ==================================================================
    # WEEKS 0-2  (Newborn period)
    # ==================================================================

    # -- motor --
    {
        "week_number": 0,
        "category": "motor",
        "title": "Flexed posture at rest",
        "description": (
            "Newborns maintain a curled, flexed posture with arms and legs "
            "drawn close to the body, reflecting normal muscle tone from "
            "the fetal position."
        ),
        "source": "AAP",
        "parent_action": (
            "Allow unrestricted movement during diaper changes to let baby "
            "stretch naturally. Avoid tight swaddling of the hips."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 0,
        "category": "motor",
        "title": "Reflexive grasp",
        "description": (
            "When you place a finger in the newborn's palm, they will "
            "reflexively close their fingers around it (palmar grasp reflex)."
        ),
        "source": "AAP",
        "parent_action": (
            "Gently place your finger in baby's palm to feel the grasp. "
            "This reflex is a sign of healthy neurological function."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 1,
        "category": "motor",
        "title": "Head turns side to side when prone",
        "description": (
            "During supervised tummy time, a newborn can briefly lift and "
            "turn their head to clear their airway. Head control is still "
            "very limited and the head must always be supported."
        ),
        "source": "AAP",
        "parent_action": (
            "Begin brief, supervised tummy-time sessions (1-2 minutes) on "
            "your chest or on a firm surface while baby is awake and alert."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 0,
        "category": "motor",
        "title": "Absent or very weak reflexes",
        "description": (
            "If the baby shows no rooting, sucking, Moro (startle), or "
            "grasp reflexes, or the reflexes are markedly asymmetric, this "
            "may indicate a neurological concern."
        ),
        "source": "AAP",
        "parent_action": (
            "Mention any absent or one-sided reflexes to your pediatrician "
            "at the first well-child visit."
        ),
        "is_concern_flag": True,
    },

    # -- sensory --
    {
        "week_number": 0,
        "category": "sensory",
        "title": "Focuses on faces at close range",
        "description": (
            "Newborns can see objects best at 8-12 inches away -- roughly "
            "the distance to a parent's face during feeding. Vision is "
            "blurry beyond this range."
        ),
        "source": "AAP",
        "parent_action": (
            "Hold your face 8-12 inches from baby during feeds and "
            "interaction. Use slow, exaggerated facial expressions."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 1,
        "category": "sensory",
        "title": "Startles to loud sounds",
        "description": (
            "The Moro (startle) reflex is triggered by sudden loud noises. "
            "Baby may throw arms outward and cry. This demonstrates intact "
            "hearing and neurological pathways."
        ),
        "source": "CDC",
        "parent_action": (
            "Observe whether baby reacts to sudden sounds. If there is no "
            "startle response by 2 weeks, mention it to your pediatrician."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 0,
        "category": "sensory",
        "title": "No response to loud sounds",
        "description": (
            "If the newborn does not startle, blink, or show any reaction "
            "to loud noises, this may indicate a hearing concern that "
            "warrants follow-up after the newborn hearing screen."
        ),
        "source": "CDC",
        "parent_action": (
            "Ensure the newborn hearing screening is completed before "
            "hospital discharge. Discuss results with your pediatrician."
        ),
        "is_concern_flag": True,
    },

    # -- communication --
    {
        "week_number": 0,
        "category": "communication",
        "title": "Crying as primary communication",
        "description": (
            "Crying is the newborn's only way to signal hunger, discomfort, "
            "tiredness, or overstimulation. Different cries may begin to "
            "sound distinct over the first weeks."
        ),
        "source": "AAP",
        "parent_action": (
            "Respond promptly to cries. You cannot spoil a newborn. Try a "
            "checklist: hungry, wet diaper, too warm/cold, needs comfort."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 2,
        "category": "communication",
        "title": "Quiets when picked up or hears a voice",
        "description": (
            "By about two weeks, many babies will briefly calm or become "
            "alert when they hear a familiar voice or are held close."
        ),
        "source": "AAP",
        "parent_action": (
            "Talk and sing to your baby frequently, even during routine "
            "care like diaper changes. Your voice is deeply soothing."
        ),
        "is_concern_flag": False,
    },

    # -- feeding --
    {
        "week_number": 0,
        "category": "feeding",
        "title": "Rooting and sucking reflexes",
        "description": (
            "When the corner of the mouth or cheek is stroked, the baby "
            "turns toward the stimulus and opens their mouth (rooting). "
            "Once latched, the sucking reflex allows feeding."
        ),
        "source": "AAP",
        "parent_action": (
            "Stroke baby's cheek gently to encourage latching during "
            "breastfeeding. If bottle-feeding, touch the nipple to the "
            "corner of the mouth."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 1,
        "category": "feeding",
        "title": "Feeds 8-12 times per 24 hours",
        "description": (
            "Newborns have small stomachs and need frequent feeds. "
            "Breastfed babies typically nurse 8-12 times; formula-fed "
            "babies take 1-2 oz every 2-3 hours in the first week."
        ),
        "source": "AAP",
        "parent_action": (
            "Feed on demand. Track wet and dirty diapers (at least 6 wet "
            "diapers/day by day 5) to confirm adequate intake."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 0,
        "category": "feeding",
        "title": "Difficulty latching or very weak suck",
        "description": (
            "Persistent inability to latch or an extremely weak suck can "
            "lead to inadequate nutrition and dehydration. This may signal "
            "tongue-tie, prematurity effects, or other concerns."
        ),
        "source": "AAP",
        "parent_action": (
            "If baby cannot sustain a latch or falls asleep immediately "
            "at every feed, contact your pediatrician or a lactation "
            "consultant within the first 48 hours."
        ),
        "is_concern_flag": True,
    },

    # -- sleep --
    {
        "week_number": 0,
        "category": "sleep",
        "title": "Sleeps 16-17 hours in short bursts",
        "description": (
            "Newborns sleep in 2-4 hour stretches around the clock with "
            "no established circadian rhythm. They wake frequently for "
            "feeding."
        ),
        "source": "AAP",
        "parent_action": (
            "Always place baby on their back on a firm, flat surface with "
            "no loose bedding. Room-share without bed-sharing for the "
            "first 6 months."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 2,
        "category": "sleep",
        "title": "Day-night confusion common",
        "description": (
            "Newborns have not yet developed a circadian rhythm and may "
            "sleep longer during the day and be more wakeful at night."
        ),
        "source": "CDC",
        "parent_action": (
            "Expose baby to natural daylight during awake periods and keep "
            "nighttime feeds calm, dim, and quiet to begin establishing "
            "day-night patterns."
        ),
        "is_concern_flag": False,
    },

    # -- social_emotional --
    {
        "week_number": 0,
        "category": "social_emotional",
        "title": "Prefers human faces",
        "description": (
            "From birth, newborns are drawn to face-like patterns and will "
            "gaze at a face longer than at other visual stimuli."
        ),
        "source": "CDC",
        "parent_action": (
            "Make plenty of face-to-face contact. Hold baby close and "
            "let them study your face during alert periods."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 2,
        "category": "social_emotional",
        "title": "Calms with skin-to-skin contact",
        "description": (
            "Skin-to-skin (kangaroo) care regulates the newborn's "
            "temperature, heart rate, and breathing while promoting "
            "bonding and reducing crying."
        ),
        "source": "WHO",
        "parent_action": (
            "Practice skin-to-skin holding daily. Place baby in just a "
            "diaper against your bare chest and cover with a blanket."
        ),
        "is_concern_flag": False,
    },

    # -- cognitive --
    {
        "week_number": 1,
        "category": "cognitive",
        "title": "Recognises parent's voice",
        "description": (
            "Research shows that newborns can distinguish their mother's "
            "voice from other voices within the first days of life, a "
            "result of prenatal auditory exposure."
        ),
        "source": "AAP",
        "parent_action": (
            "Narrate daily routines to your baby. Describe what you are "
            "doing -- this builds language exposure from day one."
        ),
        "is_concern_flag": False,
    },

    # ==================================================================
    # WEEKS 3-4
    # ==================================================================

    # -- motor --
    {
        "week_number": 3,
        "category": "motor",
        "title": "Arm and leg movements become smoother",
        "description": (
            "The jerky, uncoordinated movements of the first weeks begin "
            "to smooth out slightly as the nervous system matures."
        ),
        "source": "CDC",
        "parent_action": (
            "Give baby floor time on a blanket so they can move freely. "
            "Avoid keeping baby in a car seat or swing for extended periods."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 4,
        "category": "motor",
        "title": "Briefly lifts head during tummy time",
        "description": (
            "At about one month, many babies can lift their head at a "
            "45-degree angle for a few seconds during tummy time."
        ),
        "source": "AAP",
        "parent_action": (
            "Increase tummy time to 3-5 minutes several times a day. "
            "Get down at baby's level and talk to encourage head lifting."
        ),
        "is_concern_flag": False,
    },

    # -- sensory --
    {
        "week_number": 3,
        "category": "sensory",
        "title": "Begins to track moving objects briefly",
        "description": (
            "Baby may follow a slowly moving object or face with their "
            "eyes through a small arc (not yet full 180 degrees)."
        ),
        "source": "AAP",
        "parent_action": (
            "Slowly move a high-contrast toy or your face from side to "
            "side about 10 inches from baby's eyes and watch for tracking."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 4,
        "category": "sensory",
        "title": "Prefers bold, high-contrast patterns",
        "description": (
            "Newborn vision is best stimulated by black-and-white or "
            "high-contrast patterns, as colour vision is still immature."
        ),
        "source": "CDC",
        "parent_action": (
            "Use high-contrast cards or books during short alert periods. "
            "Hold them 8-12 inches from baby's face."
        ),
        "is_concern_flag": False,
    },

    # -- communication --
    {
        "week_number": 4,
        "category": "communication",
        "title": "Begins making small throat sounds",
        "description": (
            "Around one month, babies start making soft cooing or gurgling "
            "sounds in addition to crying -- the earliest form of "
            "pre-linguistic vocalisation."
        ),
        "source": "CDC",
        "parent_action": (
            "When baby coos, pause and respond as if having a conversation. "
            "This 'serve and return' interaction builds communication skills."
        ),
        "is_concern_flag": False,
    },

    # -- feeding --
    {
        "week_number": 3,
        "category": "feeding",
        "title": "Cluster feeding episodes",
        "description": (
            "Around 3 weeks, babies often go through a growth spurt and "
            "may want to feed very frequently (cluster feed), sometimes "
            "every hour for several hours."
        ),
        "source": "AAP",
        "parent_action": (
            "Cluster feeding is normal and helps increase milk supply. "
            "Feed on demand and ensure you stay hydrated and rested."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 4,
        "category": "feeding",
        "title": "Takes 3-4 oz per bottle feed",
        "description": (
            "Formula-fed babies at one month typically consume 3-4 ounces "
            "per feed, roughly every 3-4 hours. Breastfed babies continue "
            "on demand."
        ),
        "source": "AAP",
        "parent_action": (
            "Pace bottle feeds to prevent overfeeding: hold the bottle "
            "horizontally, allow pauses, and watch for fullness cues."
        ),
        "is_concern_flag": False,
    },

    # -- sleep --
    {
        "week_number": 4,
        "category": "sleep",
        "title": "May begin slightly longer sleep stretches at night",
        "description": (
            "Some one-month-olds start sleeping one longer stretch of "
            "3-4 hours at night, though frequent waking remains normal."
        ),
        "source": "AAP",
        "parent_action": (
            "Continue safe sleep practices. Begin a simple bedtime routine "
            "(dim lights, quiet voice, swaddle) to signal nighttime."
        ),
        "is_concern_flag": False,
    },

    # -- social_emotional --
    {
        "week_number": 4,
        "category": "social_emotional",
        "title": "First social smile may emerge",
        "description": (
            "Between 4 and 6 weeks, many babies produce their first true "
            "social smile -- a smile in direct response to a face or voice "
            "rather than a reflex."
        ),
        "source": "CDC",
        "parent_action": (
            "Smile and make animated faces when baby is calm and alert. "
            "Give them time to respond; smiling is a learned social skill."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 4,
        "category": "social_emotional",
        "title": "No social smile by 6 weeks",
        "description": (
            "If a baby has not produced any social smile by 6 weeks of "
            "age, it may be worth discussing with a pediatrician, though "
            "some healthy babies smile a bit later."
        ),
        "source": "AAP",
        "parent_action": (
            "Keep engaging face-to-face, but if no smile appears by the "
            "6-week check-up, raise it with your doctor."
        ),
        "is_concern_flag": True,
    },

    # -- cognitive --
    {
        "week_number": 3,
        "category": "cognitive",
        "title": "Distinguishes parent's scent",
        "description": (
            "By 3 weeks, babies reliably turn toward a cloth carrying "
            "their mother's scent, demonstrating early olfactory memory."
        ),
        "source": "AAP",
        "parent_action": (
            "Leave a worn t-shirt near (not in) the sleep area to provide "
            "comforting scent during brief separations."
        ),
        "is_concern_flag": False,
    },

    # ==================================================================
    # WEEKS 5-6
    # ==================================================================

    # -- motor --
    {
        "week_number": 5,
        "category": "motor",
        "title": "Holds head steadier when upright",
        "description": (
            "When held against a shoulder, the baby can keep their head "
            "upright for longer periods, though it still bobs."
        ),
        "source": "AAP",
        "parent_action": (
            "Hold baby upright on your shoulder after feeds. Continue "
            "supporting the head but let them practise control."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 6,
        "category": "motor",
        "title": "Pushes up slightly during tummy time",
        "description": (
            "Baby may push up on forearms briefly, lifting the chest a "
            "small amount off the surface during tummy time."
        ),
        "source": "CDC",
        "parent_action": (
            "Place a small rolled towel under baby's chest for support. "
            "Use toys or your face at eye level to motivate lifting."
        ),
        "is_concern_flag": False,
    },

    # -- sensory --
    {
        "week_number": 6,
        "category": "sensory",
        "title": "Tracks a moving object through 90 degrees",
        "description": (
            "Visual tracking improves so baby can follow an object or "
            "face through roughly a 90-degree arc from midline."
        ),
        "source": "AAP",
        "parent_action": (
            "Slowly move a colourful toy in an arc in front of baby. "
            "If eyes consistently fail to follow, mention it at your visit."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 6,
        "category": "sensory",
        "title": "Eyes do not follow a moving object at all",
        "description": (
            "By 6 weeks, most babies should demonstrate some visual "
            "tracking. Complete absence of tracking may indicate a visual "
            "or neurological concern."
        ),
        "source": "AAP",
        "parent_action": (
            "If baby never follows a face or object by 6 weeks, raise "
            "this with your pediatrician for evaluation."
        ),
        "is_concern_flag": True,
    },

    # -- communication --
    {
        "week_number": 5,
        "category": "communication",
        "title": "Cooing with vowel-like sounds",
        "description": (
            "Babies begin to produce 'aah' and 'ooh' sounds, especially "
            "when content and engaged with a caregiver."
        ),
        "source": "CDC",
        "parent_action": (
            "Imitate baby's sounds back to them. Wait for a response and "
            "then reply again -- this teaches conversational turn-taking."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 6,
        "category": "communication",
        "title": "Different cries for different needs",
        "description": (
            "Parents often begin to recognise distinct cries for hunger, "
            "tiredness, pain, or discomfort around this age."
        ),
        "source": "AAP",
        "parent_action": (
            "Pay attention to cry patterns. A short, rhythmic cry often "
            "means hunger; a sharp, sudden cry may signal pain."
        ),
        "is_concern_flag": False,
    },

    # -- feeding --
    {
        "week_number": 6,
        "category": "feeding",
        "title": "Growth spurt increases feeding demand",
        "description": (
            "A growth spurt around 6 weeks often causes increased hunger "
            "and fussiness. Baby may feed more frequently for 2-3 days."
        ),
        "source": "AAP",
        "parent_action": (
            "Follow baby's hunger cues and feed on demand during growth "
            "spurts. Supply will adjust within a few days."
        ),
        "is_concern_flag": False,
    },

    # -- sleep --
    {
        "week_number": 5,
        "category": "sleep",
        "title": "Begins to show drowsy cues",
        "description": (
            "Yawning, eye rubbing, looking away, and fussiness emerge as "
            "recognisable signs of sleepiness."
        ),
        "source": "AAP",
        "parent_action": (
            "Learn baby's drowsy cues and begin putting them down sleepy "
            "but awake to start building self-settling skills."
        ),
        "is_concern_flag": False,
    },

    # -- social_emotional --
    {
        "week_number": 6,
        "category": "social_emotional",
        "title": "Reliably smiles in response to faces",
        "description": (
            "By 6 weeks most babies smile deliberately in response to a "
            "parent's face and voice, marking a key social milestone."
        ),
        "source": "CDC",
        "parent_action": (
            "Smile back every time. Reciprocal smiling strengthens "
            "attachment and encourages further social development."
        ),
        "is_concern_flag": False,
    },

    # -- cognitive --
    {
        "week_number": 6,
        "category": "cognitive",
        "title": "Shows interest in novel stimuli",
        "description": (
            "Baby looks longer at new objects or sounds compared to "
            "familiar ones, demonstrating early habituation and memory."
        ),
        "source": "CDC",
        "parent_action": (
            "Introduce one new simple toy or image at a time. Rotate "
            "items to keep stimulation fresh without overwhelming baby."
        ),
        "is_concern_flag": False,
    },

    # ==================================================================
    # WEEKS 7-8  (Two months)
    # ==================================================================

    # -- motor --
    {
        "week_number": 7,
        "category": "motor",
        "title": "Holds head at 45 degrees during tummy time",
        "description": (
            "Neck and upper-back strength improves so that baby can "
            "maintain a 45-degree head lift for several seconds."
        ),
        "source": "AAP",
        "parent_action": (
            "Aim for a total of 15-30 minutes of tummy time spread "
            "throughout the day in short sessions."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 8,
        "category": "motor",
        "title": "Opens and closes hands intentionally",
        "description": (
            "The palmar grasp reflex fades and baby begins to open and "
            "close their fists on their own, exploring their hands."
        ),
        "source": "CDC",
        "parent_action": (
            "Place lightweight rattles or soft toys in baby's hand. "
            "They may hold briefly before dropping."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 8,
        "category": "motor",
        "title": "Persistent fisting with no hand opening",
        "description": (
            "If a baby keeps both hands tightly fisted at all times by "
            "8 weeks with no voluntary opening, this may suggest "
            "increased muscle tone worth evaluating."
        ),
        "source": "AAP",
        "parent_action": (
            "If baby's hands are always tightly clenched and resist "
            "gentle opening, mention it at the 2-month well visit."
        ),
        "is_concern_flag": True,
    },

    # -- sensory --
    {
        "week_number": 8,
        "category": "sensory",
        "title": "Begins to notice own hands",
        "description": (
            "Baby discovers their hands visually, staring at them as "
            "they move. This is an important step in body awareness."
        ),
        "source": "CDC",
        "parent_action": (
            "Let baby go bare-handed (no mittens) so they can see and "
            "explore their fingers."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 7,
        "category": "sensory",
        "title": "Turns head toward sounds",
        "description": (
            "Baby reliably turns their head toward a familiar voice or "
            "interesting sound, showing improved auditory localisation."
        ),
        "source": "AAP",
        "parent_action": (
            "Call baby's name from different sides and watch them turn. "
            "Use gentle rattles to encourage sound localisation."
        ),
        "is_concern_flag": False,
    },

    # -- communication --
    {
        "week_number": 8,
        "category": "communication",
        "title": "Coos and gurgles in back-and-forth exchanges",
        "description": (
            "Two-month-olds engage in proto-conversations -- cooing when "
            "spoken to, pausing, and cooing again in a turn-taking pattern."
        ),
        "source": "CDC",
        "parent_action": (
            "Have 'conversations' with baby: speak a short phrase, then "
            "wait. Respond enthusiastically when they vocalise back."
        ),
        "is_concern_flag": False,
    },

    # -- feeding --
    {
        "week_number": 8,
        "category": "feeding",
        "title": "Settles into a more predictable feeding pattern",
        "description": (
            "By 2 months many babies space feeds more evenly, roughly "
            "every 2.5-3.5 hours for breastfed and 3-4 hours for "
            "formula-fed infants."
        ),
        "source": "AAP",
        "parent_action": (
            "Continue feeding on demand, but you may notice a loose "
            "schedule emerging. Follow baby's cues, not the clock."
        ),
        "is_concern_flag": False,
    },

    # -- sleep --
    {
        "week_number": 8,
        "category": "sleep",
        "title": "One longer nighttime stretch (4-6 hours)",
        "description": (
            "Some babies begin producing one longer unbroken sleep stretch "
            "at night, often 4-6 hours, although frequent waking is still "
            "completely normal."
        ),
        "source": "AAP",
        "parent_action": (
            "Maintain a consistent bedtime routine: bath, feed, dim room, "
            "lullaby. Do not feel pressured if baby is not yet sleeping "
            "long stretches."
        ),
        "is_concern_flag": False,
    },

    # -- social_emotional --
    {
        "week_number": 8,
        "category": "social_emotional",
        "title": "Responds with excitement to familiar people",
        "description": (
            "Baby may kick legs, wave arms, and coo excitedly when a "
            "familiar caregiver approaches or speaks."
        ),
        "source": "CDC",
        "parent_action": (
            "Greet baby warmly and with enthusiasm. Narrate what you are "
            "about to do -- this builds trust and predictability."
        ),
        "is_concern_flag": False,
    },

    # -- cognitive --
    {
        "week_number": 8,
        "category": "cognitive",
        "title": "Briefly watches a toy that moves out of sight",
        "description": (
            "Baby's gaze may linger on the spot where an object "
            "disappeared for a moment, an early precursor to object "
            "permanence."
        ),
        "source": "CDC",
        "parent_action": (
            "Play gentle peek-a-boo games: cover your face briefly, "
            "then reappear with a smile."
        ),
        "is_concern_flag": False,
    },

    # ==================================================================
    # WEEKS 9-10
    # ==================================================================

    # -- motor --
    {
        "week_number": 9,
        "category": "motor",
        "title": "Bears some weight on legs when held upright",
        "description": (
            "When held in a standing position on a firm surface, baby "
            "may briefly push down with their legs."
        ),
        "source": "AAP",
        "parent_action": (
            "Support baby under the arms and let them 'stand' on your "
            "lap for a few seconds. This strengthens leg muscles."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 10,
        "category": "motor",
        "title": "Lifts head to 90 degrees during tummy time",
        "description": (
            "Baby can now push up and hold their head upright at "
            "approximately 90 degrees, looking around during tummy time."
        ),
        "source": "CDC",
        "parent_action": (
            "Place toys in a semicircle during tummy time to encourage "
            "head turning and reaching."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 10,
        "category": "motor",
        "title": "Swipes at dangling objects",
        "description": (
            "Baby begins to bat at objects hung within reach, although "
            "aiming is still imprecise."
        ),
        "source": "CDC",
        "parent_action": (
            "Use a play gym with dangling toys at chest level. "
            "Celebrate when baby connects with a toy."
        ),
        "is_concern_flag": False,
    },

    # -- sensory --
    {
        "week_number": 9,
        "category": "sensory",
        "title": "Tracks a moving object through 180 degrees",
        "description": (
            "Baby can follow a slowly moving object from one side all "
            "the way to the other, demonstrating full horizontal tracking."
        ),
        "source": "AAP",
        "parent_action": (
            "Move a toy slowly in a full arc. If eyes consistently fail "
            "to follow past midline, consult your paediatrician."
        ),
        "is_concern_flag": False,
    },

    # -- communication --
    {
        "week_number": 9,
        "category": "communication",
        "title": "Vocalises when spoken to",
        "description": (
            "Baby responds to speech directed at them with increased "
            "cooing, squealing, or vowel-like sounds."
        ),
        "source": "CDC",
        "parent_action": (
            "Use parentese (higher pitch, slower pace, exaggerated "
            "intonation) -- research shows babies attend more closely "
            "to this speech style."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 10,
        "category": "communication",
        "title": "Laughs or chuckles for the first time",
        "description": (
            "Some babies produce their first laugh between 9 and 12 weeks, "
            "often in response to playful interaction."
        ),
        "source": "CDC",
        "parent_action": (
            "Try gentle tickles, funny faces, or surprise sounds. Every "
            "baby's sense of humour is different."
        ),
        "is_concern_flag": False,
    },

    # -- feeding --
    {
        "week_number": 10,
        "category": "feeding",
        "title": "Takes 4-5 oz per bottle feed",
        "description": (
            "Formula-fed babies often increase to 4-5 ounces per feed, "
            "while breastfed babies become more efficient and may finish "
            "feeds faster."
        ),
        "source": "AAP",
        "parent_action": (
            "Watch for satiety cues: turning away, slowing sucking, or "
            "releasing the nipple. Never force baby to finish a bottle."
        ),
        "is_concern_flag": False,
    },

    # -- sleep --
    {
        "week_number": 9,
        "category": "sleep",
        "title": "Nap patterns begin to emerge",
        "description": (
            "Baby may start to consolidate daytime sleep into 3-4 "
            "somewhat predictable nap periods."
        ),
        "source": "AAP",
        "parent_action": (
            "Watch for awake windows of about 60-90 minutes. Put baby "
            "down for a nap at the first signs of tiredness."
        ),
        "is_concern_flag": False,
    },

    # -- social_emotional --
    {
        "week_number": 10,
        "category": "social_emotional",
        "title": "Shows preference for primary caregivers",
        "description": (
            "Baby clearly differentiates familiar caregivers from "
            "strangers and may fuss when held by someone unfamiliar."
        ),
        "source": "CDC",
        "parent_action": (
            "This preference is healthy. Give baby time to warm up to "
            "new people. Have the new person talk gently before holding."
        ),
        "is_concern_flag": False,
    },

    # -- cognitive --
    {
        "week_number": 9,
        "category": "cognitive",
        "title": "Anticipates routine events",
        "description": (
            "Baby may show excitement (kicking, cooing) when they "
            "recognise the start of a familiar routine such as feeding "
            "preparation."
        ),
        "source": "AAP",
        "parent_action": (
            "Keep routines consistent. Narrate steps ('Time for your "
            "bath!') to reinforce anticipation and security."
        ),
        "is_concern_flag": False,
    },

    # ==================================================================
    # WEEKS 11-12  (Three months)
    # ==================================================================

    # -- motor --
    {
        "week_number": 11,
        "category": "motor",
        "title": "Brings hands together at midline",
        "description": (
            "Baby clasps hands together in front of the body and may "
            "bring them to their mouth, showing improving coordination."
        ),
        "source": "CDC",
        "parent_action": (
            "Offer safe teething toys or rattles that baby can grasp "
            "with both hands and bring to the mouth."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 12,
        "category": "motor",
        "title": "Supports upper body on arms during tummy time",
        "description": (
            "Baby can push up on extended arms during tummy time, lifting "
            "the head and chest well off the surface."
        ),
        "source": "AAP",
        "parent_action": (
            "Encourage longer tummy-time sessions (up to 60 minutes total "
            "per day). Place motivating toys just out of reach."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 12,
        "category": "motor",
        "title": "No head control by 3 months",
        "description": (
            "If baby still has very poor head control, cannot lift the "
            "head during tummy time, or the head consistently falls to "
            "one side, this warrants evaluation."
        ),
        "source": "AAP",
        "parent_action": (
            "Discuss with your pediatrician at the 3-month or next well "
            "visit. Early physical therapy can be very effective."
        ),
        "is_concern_flag": True,
    },

    # -- sensory --
    {
        "week_number": 12,
        "category": "sensory",
        "title": "Reaches for and grasps toys",
        "description": (
            "By 3 months, many babies can coordinate looking at an object "
            "and reaching for it, sometimes successfully grasping it."
        ),
        "source": "CDC",
        "parent_action": (
            "Offer brightly coloured toys within reach. Cheer when baby "
            "successfully grasps something to encourage repetition."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 11,
        "category": "sensory",
        "title": "Eyes should move together consistently",
        "description": (
            "Occasional crossing of the eyes in the first weeks is "
            "normal, but by 3 months the eyes should align and track "
            "together. Persistent crossing (strabismus) needs evaluation."
        ),
        "source": "AAP",
        "parent_action": (
            "If one or both eyes consistently turn inward or outward, "
            "schedule an appointment with a paediatric ophthalmologist."
        ),
        "is_concern_flag": True,
    },

    # -- communication --
    {
        "week_number": 11,
        "category": "communication",
        "title": "Squeals and makes vowel strings",
        "description": (
            "Baby produces longer strings of vowel sounds ('aah-ooh-eee') "
            "and may squeal with delight."
        ),
        "source": "CDC",
        "parent_action": (
            "Mirror baby's sounds and add a new one. Read simple board "
            "books aloud, pointing at pictures."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 12,
        "category": "communication",
        "title": "Babbles with consonant-like sounds emerging",
        "description": (
            "Some babies begin to add consonant-like sounds (g, k, b) "
            "to their vowel cooing, producing early babble."
        ),
        "source": "CDC",
        "parent_action": (
            "Repeat baby's babbles back and expand on them. 'Yes, "
            "ba-ba! Are you telling me a story?'"
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 12,
        "category": "communication",
        "title": "No cooing or vocalisation by 3 months",
        "description": (
            "If baby has not produced any cooing, gurgling, or vowel "
            "sounds by 12 weeks, this may indicate a hearing or "
            "developmental concern."
        ),
        "source": "AAP",
        "parent_action": (
            "Request a hearing re-evaluation and discuss speech-language "
            "development with your pediatrician."
        ),
        "is_concern_flag": True,
    },

    # -- feeding --
    {
        "week_number": 12,
        "category": "feeding",
        "title": "Feeds become shorter and more efficient",
        "description": (
            "Breastfed babies may finish feeds in 10-15 minutes per side "
            "as they become more efficient. Formula-fed babies take "
            "about 5-6 oz per feed."
        ),
        "source": "AAP",
        "parent_action": (
            "A faster feed does not mean baby is not getting enough. "
            "Monitor weight gain and diaper output for reassurance."
        ),
        "is_concern_flag": False,
    },

    # -- sleep --
    {
        "week_number": 12,
        "category": "sleep",
        "title": "May sleep 5-6 hour stretches at night",
        "description": (
            "Many 3-month-olds can sleep a 5-6 hour stretch at night. "
            "Total sleep is roughly 14-16 hours per day including naps."
        ),
        "source": "AAP",
        "parent_action": (
            "If baby is sleeping longer at night, there is no need to "
            "wake for feeds if weight gain is on track. Continue safe "
            "sleep environment."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 11,
        "category": "sleep",
        "title": "Circadian rhythm developing",
        "description": (
            "Melatonin production begins to establish a day-night cycle. "
            "Baby starts to consolidate more sleep to nighttime hours."
        ),
        "source": "CDC",
        "parent_action": (
            "Keep mornings bright and active, evenings dim and calm. A "
            "consistent bedtime between 7-8 PM supports rhythm development."
        ),
        "is_concern_flag": False,
    },

    # -- social_emotional --
    {
        "week_number": 12,
        "category": "social_emotional",
        "title": "Enjoys interactive play",
        "description": (
            "Baby actively participates in play: smiling, laughing, "
            "vocalising, and maintaining eye contact during games."
        ),
        "source": "CDC",
        "parent_action": (
            "Play peek-a-boo, sing action songs, and make funny noises. "
            "Follow baby's lead -- if they look away, they need a break."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 12,
        "category": "social_emotional",
        "title": "Does not respond to people or smile by 3 months",
        "description": (
            "If baby rarely makes eye contact, does not smile, and shows "
            "little interest in faces or voices by 3 months, discuss "
            "this with your pediatrician."
        ),
        "source": "CDC",
        "parent_action": (
            "Bring up these observations at your next well-child visit. "
            "Early intervention services can support development."
        ),
        "is_concern_flag": True,
    },

    # -- cognitive --
    {
        "week_number": 11,
        "category": "cognitive",
        "title": "Explores cause and effect",
        "description": (
            "Baby starts to notice that their actions produce results -- "
            "batting a toy makes it move, shaking a rattle makes sound."
        ),
        "source": "CDC",
        "parent_action": (
            "Provide toys that respond to touch: rattles, crinkle toys, "
            "or play gyms with hanging elements."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 12,
        "category": "cognitive",
        "title": "Imitates some facial expressions",
        "description": (
            "Baby may try to copy an adult who opens their mouth wide "
            "or sticks out their tongue, showing early imitation ability."
        ),
        "source": "AAP",
        "parent_action": (
            "Sit face-to-face and slowly make exaggerated expressions. "
            "Give baby plenty of time to try to imitate you."
        ),
        "is_concern_flag": False,
    },
    # ==================================================================
    # WEEKS 13-14  (Entering four months)
    # ==================================================================

    # -- motor --
    {
        "week_number": 13,
        "category": "motor",
        "title": "Steadier head control when held upright",
        "description": (
            "Baby holds their head steady and centered when sitting "
            "supported or held upright, with much less wobbling."
        ),
        "source": "AAP",
        "parent_action": (
            "Practice supported sitting on your lap. Hold baby at the "
            "hips and let them work on balancing their head and trunk."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 13,
        "category": "motor",
        "title": "Reaches for objects with both hands",
        "description": (
            "Baby actively reaches for toys using both arms, though "
            "accuracy is still developing. May rake at objects with "
            "open fingers."
        ),
        "source": "CDC",
        "parent_action": (
            "Hold toys at different angles and distances to encourage "
            "reaching in various directions. Celebrate successful grabs."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 14,
        "category": "motor",
        "title": "Pushes up on extended arms during tummy time",
        "description": (
            "Baby can fully extend their arms during tummy time, "
            "lifting head and chest well off the surface and looking "
            "around with good control."
        ),
        "source": "AAP",
        "parent_action": (
            "During tummy time, place toys in a wide arc to encourage "
            "weight shifting and pivoting. Aim for 60+ minutes total per day."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 14,
        "category": "motor",
        "title": "May begin to roll from tummy to back",
        "description": (
            "Some babies make their first roll (usually tummy to back "
            "first) around this age by pushing up and tipping to one side."
        ),
        "source": "CDC",
        "parent_action": (
            "Never leave baby unattended on elevated surfaces. If baby "
            "hasn't rolled yet, that's normal — it can happen anytime "
            "between 3 and 5 months."
        ),
        "is_concern_flag": False,
    },

    # -- sensory --
    {
        "week_number": 13,
        "category": "sensory",
        "title": "Colour vision improving significantly",
        "description": (
            "Baby can now distinguish a wider range of colours and "
            "shows clear preferences for brighter, more saturated hues."
        ),
        "source": "AAP",
        "parent_action": (
            "Introduce colourful toys and board books. Point to and "
            "name colours during play — it all builds language too."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 14,
        "category": "sensory",
        "title": "Explores objects by mouthing",
        "description": (
            "Baby brings nearly everything to their mouth. Mouthing is "
            "a primary way babies explore texture, shape, and temperature "
            "at this age."
        ),
        "source": "CDC",
        "parent_action": (
            "Ensure toys are clean and too large to be a choking hazard. "
            "Offer a variety of safe textures: silicone, fabric, wood."
        ),
        "is_concern_flag": False,
    },

    # -- communication --
    {
        "week_number": 13,
        "category": "communication",
        "title": "Babbles with varied consonant-vowel combinations",
        "description": (
            "Baby produces longer babble strings mixing consonants and "
            "vowels (ba-ba, ga-ga, ma-ma) with varied intonation patterns."
        ),
        "source": "CDC",
        "parent_action": (
            "Respond to babbles as if they are real words. 'Oh, you "
            "said ba-ba! Tell me more!' This encourages continued "
            "vocalisation."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 14,
        "category": "communication",
        "title": "Squeals with delight during play",
        "description": (
            "Baby produces high-pitched squeals and excited vocalisations "
            "during enjoyable interactions, showing a growing range of "
            "emotional expression through sound."
        ),
        "source": "CDC",
        "parent_action": (
            "Play interactive games that build anticipation — like "
            "'I'm gonna get you!' with a gentle tickle at the end."
        ),
        "is_concern_flag": False,
    },

    # -- feeding --
    {
        "week_number": 13,
        "category": "feeding",
        "title": "Feeding routine well established",
        "description": (
            "Most babies have a fairly predictable feeding pattern. "
            "Breastfed babies are very efficient; formula-fed babies "
            "take about 5-6 oz per feed, 5-6 times per day."
        ),
        "source": "AAP",
        "parent_action": (
            "Continue to follow hunger cues rather than a strict schedule. "
            "Solid foods are not recommended until around 6 months."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 14,
        "category": "feeding",
        "title": "Increased distraction during feeds",
        "description": (
            "Baby becomes more aware of surroundings and may pull off "
            "the breast or bottle to look around, especially when there "
            "is activity nearby."
        ),
        "source": "AAP",
        "parent_action": (
            "Feed in a calm, quiet environment if baby is easily "
            "distracted. A nursing necklace can help maintain focus "
            "during breastfeeding."
        ),
        "is_concern_flag": False,
    },

    # -- sleep --
    {
        "week_number": 13,
        "category": "sleep",
        "title": "Sleep regression may begin",
        "description": (
            "The well-known '4-month sleep regression' often starts "
            "around 13-14 weeks as baby's sleep cycles mature to a more "
            "adult-like pattern with lighter sleep stages."
        ),
        "source": "AAP",
        "parent_action": (
            "Increased night waking is temporary and normal. Stay "
            "consistent with your bedtime routine. Avoid introducing "
            "new sleep associations out of desperation."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 14,
        "category": "sleep",
        "title": "Naps consolidating to 3-4 per day",
        "description": (
            "Daytime sleep is becoming more organised with 3-4 distinct "
            "naps. Awake windows extend to about 1.5-2 hours."
        ),
        "source": "AAP",
        "parent_action": (
            "Watch for tired cues after 1.5-2 hours of awake time. "
            "A short wind-down routine before naps (diaper change, "
            "song, dark room) can help."
        ),
        "is_concern_flag": False,
    },

    # -- social_emotional --
    {
        "week_number": 13,
        "category": "social_emotional",
        "title": "Initiates social interaction",
        "description": (
            "Baby actively seeks attention by cooing, smiling, or "
            "fussing when a caregiver is nearby but not engaging. "
            "This marks a shift from reactive to proactive socialising."
        ),
        "source": "CDC",
        "parent_action": (
            "Respond when baby 'calls' for your attention. This teaches "
            "them that communication is effective and worthwhile."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 14,
        "category": "social_emotional",
        "title": "Laughs out loud regularly",
        "description": (
            "Belly laughs become more common and baby may laugh in "
            "response to specific games, sounds, or facial expressions."
        ),
        "source": "CDC",
        "parent_action": (
            "Find what makes your baby laugh and repeat it! Common "
            "triggers: peek-a-boo, funny sounds, gentle bouncing, "
            "and blowing raspberries."
        ),
        "is_concern_flag": False,
    },

    # -- cognitive --
    {
        "week_number": 13,
        "category": "cognitive",
        "title": "Recognises familiar objects",
        "description": (
            "Baby shows recognition of familiar toys or objects by "
            "reaching for them preferentially or showing excitement "
            "when they appear."
        ),
        "source": "CDC",
        "parent_action": (
            "Keep a few favourite toys in rotation. Introduce new "
            "objects one at a time and let baby explore them thoroughly."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 14,
        "category": "cognitive",
        "title": "Watches faces intently and studies expressions",
        "description": (
            "Baby spends extended time studying facial expressions, "
            "looking from eyes to mouth and back, learning to read "
            "emotional cues."
        ),
        "source": "AAP",
        "parent_action": (
            "Use exaggerated facial expressions during interaction. "
            "Name emotions: 'Look, Mama is happy! See my big smile?'"
        ),
        "is_concern_flag": False,
    },

    # ==================================================================
    # WEEKS 15-16  (Four months)
    # ==================================================================

    # -- motor --
    {
        "week_number": 15,
        "category": "motor",
        "title": "Rolls from tummy to back consistently",
        "description": (
            "Baby can roll from front to back reliably. Some may also "
            "begin attempting to roll from back to tummy, though this "
            "typically comes a few weeks later."
        ),
        "source": "CDC",
        "parent_action": (
            "Always place baby on a safe floor surface for play. "
            "Stop swaddling for sleep if you haven't already, as baby "
            "needs free arms to roll safely."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 16,
        "category": "motor",
        "title": "Grasps objects purposefully with whole hand",
        "description": (
            "Baby uses a raking or palmar grasp to pick up toys "
            "deliberately. They can hold a toy, bring it to their "
            "mouth, and transfer it between hands with effort."
        ),
        "source": "AAP",
        "parent_action": (
            "Offer toys of different sizes and shapes. Rattles, "
            "teething rings, and soft blocks are great for practising "
            "grasp and manipulation."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 16,
        "category": "motor",
        "title": "No reaching or grasping by 4 months",
        "description": (
            "If baby is not reaching for or attempting to grasp objects "
            "by 4 months, or shows very asymmetric use of the hands, "
            "this warrants evaluation."
        ),
        "source": "AAP",
        "parent_action": (
            "Discuss with your pediatrician at the 4-month well visit. "
            "Occupational therapy referral may be recommended."
        ),
        "is_concern_flag": True,
    },
    {
        "week_number": 15,
        "category": "motor",
        "title": "Mini push-ups and pivoting during tummy time",
        "description": (
            "Baby pushes up high on extended arms and may pivot in a "
            "circle on their tummy, reaching for toys in different "
            "directions."
        ),
        "source": "CDC",
        "parent_action": (
            "Place toys in a circle around baby during tummy time to "
            "encourage pivoting. This builds core and shoulder strength "
            "needed for crawling later."
        ),
        "is_concern_flag": False,
    },

    # -- sensory --
    {
        "week_number": 15,
        "category": "sensory",
        "title": "Depth perception beginning to develop",
        "description": (
            "Binocular vision is improving and baby is starting to "
            "develop depth perception, reaching more accurately for "
            "objects at varying distances."
        ),
        "source": "AAP",
        "parent_action": (
            "Play games where you move toys closer and farther away. "
            "Stack a few soft blocks and let baby knock them over."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 16,
        "category": "sensory",
        "title": "Responds to own name",
        "description": (
            "Baby begins to turn or look when their name is called, "
            "showing they recognise the sound pattern as referring to "
            "them."
        ),
        "source": "CDC",
        "parent_action": (
            "Use your baby's name frequently during daily routines. "
            "If there is no response to name by 4 months, mention it "
            "to your pediatrician."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 16,
        "category": "sensory",
        "title": "Does not respond to sounds or own name by 4 months",
        "description": (
            "If baby consistently does not turn toward sounds or show "
            "any response when their name is called, this may indicate "
            "a hearing concern."
        ),
        "source": "AAP",
        "parent_action": (
            "Request a hearing evaluation from your pediatrician. "
            "Early detection of hearing issues is critical for speech "
            "and language development."
        ),
        "is_concern_flag": True,
    },

    # -- communication --
    {
        "week_number": 15,
        "category": "communication",
        "title": "Babbling becomes more speech-like",
        "description": (
            "Baby's babbling takes on the rhythm and intonation of real "
            "speech, with rising and falling pitch patterns that sound "
            "like questions and statements."
        ),
        "source": "CDC",
        "parent_action": (
            "Have 'conversations' where you respond to baby's babble "
            "as though they said something meaningful. This teaches "
            "conversational rhythm."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 16,
        "category": "communication",
        "title": "Blows raspberries and experiments with lip sounds",
        "description": (
            "Baby discovers they can make sounds with their lips — "
            "blowing raspberries, smacking lips, and making 'brrr' "
            "sounds. This builds oral motor control for later speech."
        ),
        "source": "CDC",
        "parent_action": (
            "Blow raspberries back! This is great oral motor practice "
            "and babies find it hilarious. It also exercises muscles "
            "used in feeding and future speech."
        ),
        "is_concern_flag": False,
    },

    # -- feeding --
    {
        "week_number": 15,
        "category": "feeding",
        "title": "Shows interest in what others are eating",
        "description": (
            "Baby may watch intently when others eat, follow food from "
            "plate to mouth, and open their mouth in imitation. This "
            "does not mean they are ready for solids yet."
        ),
        "source": "AAP",
        "parent_action": (
            "Interest in food is normal but not a readiness sign on "
            "its own. Wait until around 6 months and when baby can "
            "sit with support before starting solids."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 16,
        "category": "feeding",
        "title": "Takes 6-8 oz per bottle feed",
        "description": (
            "Formula-fed babies typically take 6-8 ounces per feed, "
            "4-5 times per day. Breastfed babies continue to self-"
            "regulate efficiently at the breast."
        ),
        "source": "AAP",
        "parent_action": (
            "Total daily intake should be around 24-32 oz of formula "
            "or equivalent breast milk. Continue to follow baby's cues "
            "rather than forcing amounts."
        ),
        "is_concern_flag": False,
    },

    # -- sleep --
    {
        "week_number": 15,
        "category": "sleep",
        "title": "4-month sleep regression may peak",
        "description": (
            "Sleep disruption from maturing sleep cycles may peak "
            "around 15-16 weeks. Baby may wake more frequently and "
            "have difficulty falling back to sleep."
        ),
        "source": "AAP",
        "parent_action": (
            "Stay consistent with routines. This regression is "
            "permanent brain maturation, not a phase to 'get through.' "
            "It's a good time to focus on healthy sleep habits."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 16,
        "category": "sleep",
        "title": "Total sleep around 14-15 hours per day",
        "description": (
            "By 4 months, most babies sleep 10-12 hours at night "
            "(with wakings) and 3-4 hours during the day across "
            "3-4 naps."
        ),
        "source": "AAP",
        "parent_action": (
            "If night sleep is very disrupted, ensure baby is getting "
            "enough daytime sleep. An overtired baby actually sleeps "
            "worse at night."
        ),
        "is_concern_flag": False,
    },

    # -- social_emotional --
    {
        "week_number": 15,
        "category": "social_emotional",
        "title": "Shows a range of emotions clearly",
        "description": (
            "Baby's emotional expressions become more distinct and "
            "readable — joy, frustration, excitement, boredom, and "
            "displeasure are all clearly communicated."
        ),
        "source": "CDC",
        "parent_action": (
            "Name baby's emotions as you see them: 'You look frustrated! "
            "Let me help.' This builds emotional vocabulary over time."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 16,
        "category": "social_emotional",
        "title": "Enjoys looking at self in mirror",
        "description": (
            "Baby is fascinated by their reflection, smiling, cooing, "
            "and reaching toward the mirror. They don't yet recognise "
            "it as themselves."
        ),
        "source": "CDC",
        "parent_action": (
            "Place an unbreakable baby mirror at tummy-time level. "
            "Sit together in front of a mirror and point out features: "
            "'There's your nose!'"
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 16,
        "category": "social_emotional",
        "title": "No social engagement or emotional expression by 4 months",
        "description": (
            "If baby rarely smiles, does not laugh, shows no interest "
            "in people, or does not express a range of emotions by "
            "4 months, this should be discussed with your pediatrician."
        ),
        "source": "AAP",
        "parent_action": (
            "Raise these observations at the 4-month well visit. "
            "Your pediatrician may recommend developmental screening."
        ),
        "is_concern_flag": True,
    },

    # -- cognitive --
    {
        "week_number": 15,
        "category": "cognitive",
        "title": "Improved hand-eye coordination",
        "description": (
            "Baby can see a toy, reach for it, and grasp it in one "
            "smooth motion — a significant coordination milestone "
            "combining vision and motor planning."
        ),
        "source": "CDC",
        "parent_action": (
            "Offer toys at varying distances and angles. Let baby "
            "practise reaching while lying on their back, sitting "
            "supported, and during tummy time."
        ),
        "is_concern_flag": False,
    },
    {
        "week_number": 16,
        "category": "cognitive",
        "title": "Begins to show memory for people and places",
        "description": (
            "Baby may show excitement when arriving at a familiar "
            "place or seeing a regular caregiver, indicating growing "
            "memory capacity."
        ),
        "source": "AAP",
        "parent_action": (
            "Narrate your routines and where you are going. 'We're "
            "going to Grandma's house!' Familiar narration strengthens "
            "memory associations."
        ),
        "is_concern_flag": False,
    },
]


# ---------------------------------------------------------------------------
# Seed function
# ---------------------------------------------------------------------------

def seed():
    """Insert milestone data into the database."""
    print("Creating tables if they do not exist...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing = db.query(Milestone).count()
        if existing > 0:
            print(
                f"Database already contains {existing} milestones. "
                "Skipping seed to avoid duplicates."
            )
            return

        print(f"Preparing {len(MILESTONES)} milestones for insertion...")

        milestone_objects = [Milestone(**data) for data in MILESTONES]

        # Summarise what we are about to insert
        categories = {}
        weeks = set()
        concern_count = 0
        for m in MILESTONES:
            cat = m["category"]
            categories[cat] = categories.get(cat, 0) + 1
            weeks.add(m["week_number"])
            if m.get("is_concern_flag"):
                concern_count += 1

        print(f"  Weeks covered  : {sorted(weeks)}")
        print(f"  Categories     : {dict(sorted(categories.items()))}")
        print(f"  Concern flags  : {concern_count}")

        db.add_all(milestone_objects)
        db.commit()

        final_count = db.query(Milestone).count()
        print(f"Successfully seeded {final_count} milestones.")
    except Exception as exc:
        db.rollback()
        print(f"Error during seeding: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
