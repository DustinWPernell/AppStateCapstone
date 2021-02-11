-- phpMyAdmin SQL Dump
-- version 4.9.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jan 21, 2021 at 04:00 PM
-- Server version: 5.7.26-29-log
-- PHP Version: 7.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `userdb`
--
CREATE DATABASE IF NOT EXISTS `userdb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `userdb`;

-- --------------------------------------------------------

--
-- Table structure for table `AcctType`
--

CREATE TABLE `AcctType` (
  `ID` int(11) NOT NULL,
  `Display` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `AcctType`
--

INSERT INTO `AcctType` (`ID`, `Display`) VALUES
(1, 'Admin'),
(2, 'StdUser'),
(3, 'AdvUser');

-- --------------------------------------------------------

--
-- Table structure for table `FriendList`
--

CREATE TABLE `FriendList` (
  `ID` int(11) NOT NULL,
  `UserOne` int(11) NOT NULL,
  `UserTwo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

CREATE TABLE `Users` (
  `ID` int(11) NOT NULL,
  `UserName` varchar(50) NOT NULL,
  `DisplayName` varchar(50) NOT NULL,
  `Email` varchar(150) NOT NULL,
  `Password` varchar(50) NOT NULL,
  `AcctType` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Users`
--

INSERT INTO `Users` (`ID`, `UserName`, `DisplayName`, `Email`, `Password`, `AcctType`) VALUES
(2, 'Dustin', 'TechWiz', 'pernelldusty@gmail.com', 'Abc123!!', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `AcctType`
--
ALTER TABLE `AcctType`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `FriendList`
--
ALTER TABLE `FriendList`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `AcctType` (`AcctType`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `AcctType`
--
ALTER TABLE `AcctType`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `FriendList`
--
ALTER TABLE `FriendList`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Users`
--
ALTER TABLE `Users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Users`
--
ALTER TABLE `Users`
  ADD CONSTRAINT `Users_ibfk_1` FOREIGN KEY (`AcctType`) REFERENCES `AcctType` (`ID`);
--
-- Database: `carddb`
--
CREATE DATABASE IF NOT EXISTS `carddb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `carddb`;

-- --------------------------------------------------------

--
-- Table structure for table `Artists`
--

CREATE TABLE `Artists` (
  `ID` int(11) NOT NULL,
  `Name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Artists`
--

INSERT INTO `Artists` (`ID`, `Name`) VALUES
(1, 'Aaron Boyd'),
(2, 'Aaron Miller'),
(3, 'Adam Paquette'),
(4, 'Adam Rex'),
(5, 'Adi Granov'),
(6, 'Adrian Majkrzak'),
(7, 'Adrian Smith'),
(8, 'Ai Desheng'),
(9, 'Al Davidson'),
(10, 'Alan Pollack'),
(11, 'Alan Rabinowitz'),
(12, 'Alayna Danner'),
(13, 'Alejandro Mirabal'),
(14, 'Aleksi Briclot'),
(15, 'Alex Brock'),
(16, 'Alex Horley-Orlandelli'),
(17, 'Alex Konstad'),
(18, 'Alexander Forssberg'),
(19, 'Alisa Lee'),
(20, 'Allen Williams'),
(21, 'Allison Carl'),
(22, 'Alton Lawson'),
(23, 'Amy Weber'),
(24, 'Anastasia Ovchinnikova'),
(25, 'Andi Rusu'),
(26, 'Andrea Radeck'),
(27, 'Andreas Rocha'),
(28, 'Andrew Goldhawk'),
(29, 'Andrew Murray'),
(30, 'Andrew Robinson'),
(31, 'Andrey Kuzinskiy'),
(32, 'Anna Podedworna'),
(33, 'Anna Steinbauer'),
(34, 'Anson Maddocks'),
(35, 'Anthony Francisco'),
(36, 'Anthony Jones'),
(37, 'Anthony Palumbo'),
(38, 'Anthony S. Waters'),
(39, 'Antonio José Manzanedo'),
(40, 'April Lee'),
(41, 'Ariel Olivetti'),
(42, 'Arnie Swekel'),
(43, 'Ash Wood'),
(44, 'Austin Hsu'),
(45, 'Babyson Chen & Uzhen Lin'),
(46, 'Bartłomiej Gaweł'),
(47, 'Bastien L. Deharme'),
(48, 'Bayard Wu'),
(49, 'BD'),
(50, 'Ben Maier'),
(51, 'Ben Thompson'),
(52, 'Ben Wootten'),
(53, 'Berry'),
(54, 'Bill Sienkiewicz'),
(55, 'Billy Christian'),
(56, 'Blackie del Rio'),
(57, 'Bob Eggleton'),
(58, 'Bob Petillo'),
(59, 'Brad Rigney'),
(60, 'Bradley Williams'),
(61, 'Bram Sels'),
(62, 'Brandon Dorman'),
(63, 'Brandon Kitkouski'),
(64, 'Brian Despain'),
(65, 'Brian Durfee'),
(66, 'Brian Horton'),
(67, 'Brian Snøddy'),
(68, 'Brian Valeza'),
(69, 'Brom'),
(70, 'Bryan Sola'),
(71, 'Bryan Talbot'),
(72, 'Brynn Metheney'),
(73, 'Bryon Wackwitz'),
(74, 'Bud Cook'),
(75, 'Cai Tingting'),
(76, 'Cara Mitten'),
(77, 'Carl Critchlow'),
(78, 'Carl Frank'),
(79, 'Carol Heyer'),
(80, 'Catherine Buck'),
(81, 'Cecil Fernando'),
(82, 'Charles Gillespie'),
(83, 'Chase Stone'),
(84, 'Chen Weidong'),
(85, 'Chengo McFlingers'),
(86, 'Chippy'),
(87, 'Chris Appelhans'),
(88, 'Chris Dien'),
(89, 'Chris Rahn'),
(90, 'Chris Rallis'),
(91, 'Christine Choi'),
(92, 'Christopher Burdett'),
(93, 'Christopher Moeller'),
(94, 'Christopher Rush'),
(95, 'Chuck Lukacs'),
(96, 'Ciruelo Cabral'),
(97, 'Cliff Childs'),
(98, 'Cliff Nielsen'),
(99, 'Clint Cearley'),
(100, 'Clint Langley'),
(101, 'Clyde Caldwell'),
(102, 'Cole Eastburn'),
(103, 'Colin MacNeil'),
(104, 'Corey D. Macourek'),
(105, 'Cornelius Brudi'),
(106, 'Craig Hooper'),
(107, 'Craig J. Spearing'),
(108, 'Craig Mullins'),
(109, 'Cris Dornaus'),
(110, 'Cynthia Sheppard'),
(111, 'Cyril van der Haegen'),
(112, 'D. Alexander Gregory'),
(113, 'D. J. Cleland-Hura'),
(114, 'Daarken'),
(115, 'Dameon Willich'),
(116, 'Dan Dos Santos'),
(117, 'Dan Frazier'),
(118, 'Dan Scott'),
(119, 'Dan Seagrave'),
(120, 'Dana Knutson'),
(121, 'Daniel Gelon'),
(122, 'Daniel Ljunggren'),
(123, 'Daniel R. Horne'),
(124, 'Darbury Stenderu'),
(125, 'Darek Zabrocki'),
(126, 'Daren Bader'),
(127, 'Darrell Riche'),
(128, 'Dave Allsop'),
(129, 'Dave DeVries'),
(130, 'Dave Dorman'),
(131, 'Dave Kendall'),
(132, 'Dave Seeley'),
(133, 'David A. Cherry'),
(134, 'David Day'),
(135, 'David Gaillet'),
(136, 'David Ho'),
(137, 'David Horne'),
(138, 'David Hudnut'),
(139, 'David Martin'),
(140, 'David Monette'),
(141, 'David O\'Connor'),
(142, 'David Palumbo'),
(143, 'David Rapoza'),
(144, 'David Seguin'),
(145, 'Dennis Detwiller'),
(146, 'Dermot Power'),
(147, 'Deruchenko Alexander'),
(148, 'Diana Vick'),
(149, 'Ding Songjian'),
(150, 'Dom!'),
(151, 'Dominick Domingo'),
(152, 'Don Hazeltine'),
(153, 'Donato Giancola'),
(154, 'Doug Chaffee'),
(155, 'Douglas Shuler'),
(156, 'Drew Tucker'),
(157, 'Dylan Martens'),
(158, 'E. M. Gist'),
(159, 'Edward P. Beard Jr.'),
(160, 'Efflam Mercier'),
(161, 'Efrem Palacios'),
(162, 'Eric David Anderson'),
(163, 'Eric Fortune'),
(164, 'Eric Peterson'),
(165, 'Eric Polak'),
(166, 'Eric Velhagen'),
(167, 'Erica Yang'),
(168, 'Esad Ribic'),
(169, 'Evan Shipard'),
(170, 'Eytan Zana'),
(171, 'Fang Yue'),
(172, 'Fay Jones'),
(173, 'Filip Burburan'),
(174, 'Florian de Gesincourt'),
(175, 'Francis Tsai'),
(176, 'Frank Kelly Freas'),
(177, 'Franz Vohwinkel'),
(178, 'Fred Fields'),
(179, 'Fred Harper'),
(180, 'Fred Rahmqvist'),
(181, 'Gabor Szikszai'),
(182, 'Gao Jianzhang'),
(183, 'Gao Yan'),
(184, 'Garry Leach'),
(185, 'Gary Ruddell'),
(186, 'Geofrey Darrow'),
(187, 'George Pratt'),
(188, 'Brom'),
(189, 'Gerry Grace'),
(190, 'Glen Angus'),
(191, 'Glenn Fabry'),
(192, 'Goran Josic'),
(193, 'Greg Hildebrandt'),
(194, 'Greg Opalinski'),
(195, 'Greg Simanson'),
(196, 'Greg Spalenka'),
(197, 'Greg Staples'),
(198, 'Grzegorz Rutkowski'),
(199, 'Hannibal King'),
(200, 'Harold McNeill'),
(201, 'He Jiancheng'),
(202, 'Erica Gassalasca-Jape'),
(203, 'Heather Hudson'),
(204, 'Henry G. Higgenbotham'),
(205, 'Henry van der Linde'),
(206, 'Hideaki Takamura'),
(207, 'Hiro Izawa'),
(208, 'Hong Yan'),
(209, 'Howard Lyon'),
(210, 'Huang Qishi'),
(211, 'Hugh Jamieson'),
(212, 'I. Rabarot'),
(213, 'Iain McCaig'),
(214, 'Ian Miller'),
(215, 'Igor Kieryluk'),
(216, 'Ittoku'),
(217, 'Izzy \"Izzy\" Medrano'),
(218, 'Jack Wang'),
(219, 'Jack Wei'),
(220, 'Jacques Bredy'),
(221, 'Jaime Jones'),
(222, 'Jakub Kasper'),
(223, 'Jama Jurabaev'),
(224, 'James Ernest'),
(225, 'James Kei'),
(226, 'James Paick'),
(227, 'James Ryman'),
(228, 'James Zapata'),
(229, 'Janet Aulisio'),
(230, 'Janine Johnston'),
(231, 'Jarreau Wimberly'),
(232, 'Jason A. Engle'),
(233, 'Jason Alexander Behnke'),
(234, 'Jason Chan'),
(235, 'Jason Felix'),
(236, 'Jason Kang'),
(237, 'Jason Rainville'),
(238, 'Jasper Sandner'),
(239, 'Jean-Sébastien Rossbach'),
(240, 'Jeff A. Menges'),
(241, 'Jeff Easley'),
(242, 'Jeff Laubenstein'),
(243, 'Jeff Miracola'),
(244, 'Jeff Nentrup'),
(245, 'Jeff Reitz'),
(246, 'Jeff Remmer'),
(247, 'Jeff Simpson'),
(248, 'Jeffrey R. Busch'),
(249, 'Jehan Choo'),
(250, 'Jen Page'),
(251, 'Jennifer Law'),
(252, 'Jeremy Enecio'),
(253, 'Jeremy Jarvis'),
(254, 'Jerry Tiritilli'),
(255, 'Jesper Ejsing'),
(256, 'Jesper Myrfors'),
(257, 'Ji Yong'),
(258, 'Jiaming'),
(259, 'Jiang Zhuqing'),
(260, 'Jim Murray'),
(261, 'Jim Nelson'),
(262, 'Jim Pavelec'),
(263, 'Mark \"JOCK\" Simpson'),
(264, 'Joel Biske'),
(265, 'Joel Thomas'),
(266, 'Johann Bodin'),
(267, 'Johannes Voss'),
(268, 'John Avon'),
(269, 'John Bolton'),
(270, 'John Coulthart'),
(271, 'John Donahue'),
(272, 'John Gallagher'),
(273, 'John Howe'),
(274, 'John Malloy'),
(275, 'John Matson'),
(276, 'John Severin Brassell'),
(277, 'John Stanko'),
(278, 'John Zeleznik'),
(279, 'Jon Foster'),
(280, 'Jon J. Muth'),
(281, 'Jonas De Ro'),
(282, 'Jonathan Kuo'),
(283, 'Jose Cabrera'),
(284, 'Joseph Meehan'),
(285, 'Josh Hass'),
(286, 'Joshua Hagler'),
(287, 'Josu Hernaiz'),
(288, 'Julie Baroh'),
(289, 'Jung Park'),
(290, 'Junich Inoue'),
(291, 'Junior Tomlin'),
(292, 'Junko Taguchi'),
(293, 'Justin Hampton'),
(294, 'Justin Murray'),
(295, 'Justin Sweet'),
(296, 'Kaja Foglio'),
(297, 'Kang Yu'),
(298, 'Kari Johnson'),
(299, 'Karl Kopinski'),
(300, 'Karla Ortiz'),
(301, 'Kathryn Rathke'),
(302, 'Keith Garletts'),
(303, 'Keith Parkinson'),
(304, 'Kensuke Okabayashi'),
(305, 'Kerstin Kaman'),
(306, 'Kev Brockschmidt'),
(307, 'Kevin \"Kev\" Walker'),
(308, 'Kevin Dobler'),
(309, 'Kevin Murphy'),
(310, 'Khang Le'),
(311, 'Kieran Yanner'),
(312, 'Kipling West'),
(313, 'Kirsten Zirngibl'),
(314, 'Koji'),
(315, 'Kristen Bishop'),
(316, 'Ku Xueming'),
(317, 'Kuang Sheng'),
(318, 'L. A. Williams'),
(319, 'LHQ'),
(320, 'Lake Hurwitz'),
(321, 'Larry Elmore'),
(322, 'Larry MacDougall'),
(323, 'Lars Grant-West'),
(324, 'Lawrence Snelly'),
(325, 'Li Tie'),
(326, 'Li Wang'),
(327, 'Li Xiaohua'),
(328, 'Li Youliang'),
(329, 'Li Yousong'),
(330, 'Lie Tiu'),
(331, 'Lin Yan'),
(332, 'Lindsey Look'),
(333, 'Liu Jianjian'),
(334, 'Liu Shangying'),
(335, 'Lius Lasahido'),
(336, 'Liz Danforth'),
(337, 'Lou Harrison'),
(338, 'Lubov'),
(339, 'Luca Zontini'),
(340, 'Lucas Graciano'),
(341, 'Lucio Parrillo'),
(342, 'M. W. Kaluta'),
(343, 'Magali Villeneuve'),
(344, 'Marc Fishman'),
(345, 'Marc Simonetti'),
(346, 'Marcelo Vignali'),
(347, 'Marco Nelor'),
(348, 'Margaret Organ-Kean'),
(349, 'Mark Brill'),
(350, 'Mark Harrison'),
(351, 'Mark A. Nelson'),
(352, 'Mark Poole'),
(353, 'Mark Romanoski'),
(354, 'Mark Rosewater'),
(355, 'Mark Tedin'),
(356, 'Mark Winters'),
(357, 'Mark Zug'),
(358, 'Martin McKenna'),
(359, 'Massimilano Frezzato'),
(360, 'Mathias Kollros'),
(361, 'Matt Cavotta'),
(362, 'Matt Stawicki'),
(363, 'Matt Stewart'),
(364, 'Matt Thompson'),
(365, 'Matthew D. Wilson'),
(366, 'Matthew Mitchell'),
(367, 'Melissa A. Benson'),
(368, 'Miao Aili'),
(369, 'Michael Bruinsma'),
(370, 'Michael Danza'),
(371, 'Michael Koelsch'),
(372, 'Michael Komarck'),
(373, 'Michael Phillippi'),
(374, 'Michael Ryan'),
(375, 'Michael Sutfin'),
(376, 'Michael Weaver'),
(377, 'Michael Whelan'),
(378, 'Mike Bierek'),
(379, 'Mike Dringenberg'),
(380, 'Mike Kerr'),
(381, 'Mike Kimble'),
(382, 'Mike Ploog'),
(383, 'Mike Raabe'),
(384, 'Mike Sass'),
(385, 'Min Yum'),
(386, 'Mitch Cotie'),
(387, 'Mitsuaki Sagiri'),
(388, 'Monte Michael Moore'),
(389, 'Naomi Baker'),
(390, 'Nathalie Hertz'),
(391, 'Nelson DeCastro'),
(392, 'Nene Thomas'),
(393, 'Nick Percival'),
(394, 'Nicola Leonard'),
(395, 'Nils Hamm'),
(396, 'Noah Bradley'),
(397, 'Nottsuo'),
(398, 'Omaha Pérez'),
(399, 'Omar Rayyan'),
(400, 'Paolo Parente'),
(401, 'Pat Lee'),
(402, 'Pat Morrissey'),
(403, 'Patrick Beel'),
(404, 'Patrick Ho'),
(405, 'Patrick Kochakji'),
(406, 'Paul Bonner'),
(407, 'Paul Chadwick'),
(408, 'Paul Lee'),
(409, 'Pete Venters'),
(410, 'Peter Bollinger'),
(411, 'Peter Mohrbacher'),
(412, 'Phil Foglio'),
(413, 'Philip Mosness'),
(414, 'Philip Straub'),
(415, 'Philip Tan'),
(416, 'Phill Simmer'),
(417, 'Piotr Dura'),
(418, 'Puddnhead'),
(419, 'Qi Baocheng'),
(420, 'Qiao Dafu'),
(421, 'Qin Jun'),
(422, 'Qu Xin'),
(423, 'Quan Xuejun'),
(424, 'Quinton Hoover'),
(425, 'Raf Sarmento'),
(426, 'Ralph Horsley'),
(427, 'Randy Asplund-Faith'),
(428, 'Randy Elliott'),
(429, 'Randy Gallegos'),
(430, 'Randy \"rk\" Post'),
(431, 'Randy Vargas'),
(432, 'Raoul Vitale'),
(433, 'Ray Lago'),
(434, 'Raymond Swanland'),
(435, 'Rebecca Guay'),
(436, 'Rebekah Lynn'),
(437, 'Richard Kane Ferguson'),
(438, 'Richard Sardinha'),
(439, 'Richard Thomas'),
(440, 'Richard Whitters'),
(441, 'Richard Wright'),
(442, 'Rick Berry'),
(443, 'Rick Emond'),
(444, 'Rick Farrell'),
(445, 'Rob Alexander'),
(446, 'Robert Bliss'),
(447, 'Robh Ruppel'),
(448, 'Roger Raupp'),
(449, 'Rogério Vilela'),
(450, 'Romas Kukalis'),
(451, 'Ron Brown'),
(452, 'Ron Chironna'),
(453, 'Ron Spencer'),
(454, 'Ron Walotsky'),
(455, 'Ruth Thompson'),
(456, 'Ryan Alexander Lee'),
(457, 'Ryan Barger'),
(458, 'Ryan Pancoast'),
(459, 'Ryan Yee'),
(460, 'Sal Villagran'),
(461, 'Sam Wood'),
(462, 'Sandra Everingham'),
(463, 'Sara Winters'),
(464, 'Scott Altmann'),
(465, 'Scott Bailey'),
(466, 'Scott M. Fischer'),
(467, 'Scott Hampton'),
(468, 'Scott Kirschner'),
(469, 'Scott Murphy'),
(470, 'Sean McConnell'),
(471, 'Sean Murray'),
(472, 'Sean Sevestre'),
(473, 'Seb McKinnon'),
(474, 'Shang Huitong'),
(475, 'Shelly Wan'),
(476, 'Shishizaru'),
(477, 'Sidharth Chaturvedi'),
(478, 'Slawomir Maniak'),
(479, 'Solomon Au Yeung'),
(480, 'Song Shikai'),
(481, 'Stephanie Pui-Mun Law'),
(482, 'Stephen Daniele'),
(483, 'Stephen L. Walsh'),
(484, 'Steve Argyle'),
(485, 'Steve Ellis'),
(486, 'Steve Firchow'),
(487, 'Steve Luke'),
(488, 'Steve Prescott'),
(489, 'Steve White'),
(490, 'Steven Belledin'),
(491, 'Stuart Griffin'),
(492, 'Sue Ellen Brown'),
(493, 'Sun Nan'),
(494, 'Sung Choi'),
(495, 'Susan Van Camp'),
(496, 'Svetlin Velinov'),
(497, 'Tang Xiaogu'),
(498, 'Ted Naifeh'),
(499, 'Terese Nielsen'),
(500, 'Terry Springer'),
(501, 'Thomas M. Baxa'),
(502, 'Thomas Denmark'),
(503, 'Thomas Gianni'),
(504, 'Tianhua Xu'),
(505, 'Tim Hildebrandt'),
(506, 'Titus Lunter'),
(507, 'Todd Lockwood'),
(508, 'Tom Babbey'),
(509, 'Tom Fleming'),
(510, 'Tom Kyffin'),
(511, 'Tom Wänerstrand'),
(512, 'Tomas Giorello'),
(513, 'Tomasz Jedruszek'),
(514, 'Tommy Arnold'),
(515, 'Tony DiTerlizzi'),
(516, 'Tony Foti'),
(517, 'Tony Roberts'),
(518, 'Tony Szczudlo'),
(519, 'Torstein Nordstrand'),
(520, 'Trevor Claxton'),
(521, 'Trevor Hairsine'),
(522, 'Tsutomu Kawade'),
(523, 'Tyler Jacobson'),
(524, 'Una Fricker'),
(525, 'Val Mayerik'),
(526, 'Vance Kovacs'),
(527, 'Victor Adame Minguez'),
(528, 'Viktor Titov'),
(529, 'Vincent Evans'),
(530, 'Vincent Proce'),
(531, 'Volkan Baga'),
(532, 'Wang Chuxiong'),
(533, 'Wang Feng'),
(534, 'Wang Yuqun'),
(535, 'Warren Mahy'),
(536, 'Wayne England'),
(537, 'Wayne Reynolds'),
(538, 'Wesley Burt'),
(539, 'William Donohoe'),
(540, 'William O\'Connor'),
(541, 'William Simpson'),
(542, 'Willian Murai'),
(543, 'Winona Nelson'),
(544, 'Xi Zhang'),
(545, 'Xu Tan'),
(546, 'Xu Xiaoming'),
(547, 'YW Tang'),
(548, 'Yan Li'),
(549, 'Yang Guangmai'),
(550, 'Yang Hong'),
(551, 'Yang Jun Kwon'),
(552, 'Yefim Kligerman'),
(553, 'Yeong-Hao Han'),
(554, 'Yohann Schepacz'),
(555, 'Yokota Katsumi'),
(556, 'Zack Stella'),
(557, 'Zak Plucinski'),
(558, 'Zezhou Chen'),
(559, 'Zhang Jiazhen'),
(560, 'Zhao Dafu'),
(561, 'Zhao Tan'),
(562, 'Zina Saunders'),
(563, 'Zoltan Boros'),
(564, 'Evyn Fong'),
(565, 'Sam Burley'),
(566, 'Yongjae Choi'),
(567, 'Martina Pilcerova'),
(568, 'Eric Deschamps'),
(569, 'Campbell White'),
(570, 'Mila Pesic'),
(571, 'Livia Prima'),
(572, 'Zoltan Boros & Gabor Szikszai'),
(573, 'Dimitar Marinski'),
(574, 'Kev Walker'),
(575, 'Stephan Martiniere'),
(576, 'Greg Hilderbrandt'),
(577, 'Heonhwa Choe'),
(578, 'Milivoj Ćeran'),
(579, 'Simon Dominic'),
(580, 'Nicholas Gregory'),
(581, 'Jermey Wilson');

-- --------------------------------------------------------

--
-- Table structure for table `Card`
--

CREATE TABLE `Card` (
  `ID` int(11) NOT NULL,
  `Name` varchar(50) NOT NULL,
  `MultiverseID` int(11) NOT NULL,
  `SetID` int(11) NOT NULL,
  `SetNum` int(11) NOT NULL,
  `ManaCost` int(11) NOT NULL,
  `ColorID` int(11) NOT NULL,
  `Rarity` varchar(20) NOT NULL,
  `Power` int(11) NOT NULL,
  `Toughness` int(11) NOT NULL,
  `ArtistID` int(11) NOT NULL,
  `Description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `CardSet`
--

CREATE TABLE `CardSet` (
  `ID` int(11) NOT NULL,
  `Name` varchar(50) NOT NULL,
  `Year` int(11) NOT NULL,
  `Code` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `CardSet`
--

INSERT INTO `CardSet` (`ID`, `Name`, `Year`, `Code`) VALUES
(1, 'Alpha (Limited Edition)', 1993, 'LEA'),
(2, 'Beta (Limited Edition)', 1993, 'LEB'),
(3, 'Unlimited Edition', 1993, '2ED'),
(4, 'Arabian Nights', 1993, 'ARN'),
(5, 'Antiquities', 1994, 'ATQ'),
(6, 'Revised Edition', 1994, '3ED'),
(7, 'Legends', 1994, 'LEG'),
(8, 'The Dark', 1994, 'DRK'),
(9, 'Fallen Empires', 1994, 'FEM'),
(10, 'Fourth Edition', 1995, '4ED'),
(11, 'Ice Age', 1995, 'ICE'),
(12, 'Chronicles', 1995, 'CHR'),
(13, 'Renaissance', 1995, ''),
(14, 'Homelands', 1995, 'HML'),
(15, 'Alliances', 1996, 'ALL'),
(16, 'Mirage', 1996, 'MIR'),
(17, 'Visions', 1997, 'VIS'),
(18, 'Fifth Edition', 1997, '5ED'),
(19, 'Portal', 1997, 'POR'),
(20, 'Weatherlight', 1997, 'WTH'),
(21, 'Tempest', 1997, 'TMP'),
(22, 'Stronghold', 1998, 'STH'),
(23, 'Exodus', 1998, 'EXO'),
(24, 'Portal Second Age', 1998, 'P02'),
(25, 'Unglued', 1998, 'UGL'),
(26, 'Urza\'s Saga', 1998, 'USG'),
(27, 'Anthologies', 1998, 'ATH'),
(28, 'Urza\'s Legacy', 1999, 'ULG'),
(29, 'Sixth Edition', 1999, '6ED'),
(30, 'Portal Three Kingdoms', 1999, 'PTK'),
(31, 'Urza\'s Destiny', 1999, 'UDS'),
(32, 'Starter 1999', 1999, 'S99'),
(33, 'Mercadian Masques', 1999, 'MMQ'),
(34, 'Battle Royale', 1999, 'BRB'),
(35, 'Nemesis', 2000, 'NEM'),
(36, 'Starter 2000', 2000, '200'),
(37, 'Prophecy', 2000, 'PCY'),
(38, 'Invasion', 2000, 'INV'),
(39, 'Beatdown', 2000, 'BTD'),
(40, 'Planeshift', 2001, 'PLS'),
(41, 'Seventh Edition', 2001, '7ED'),
(42, 'Apocalypse', 2001, 'APC'),
(43, 'Odyssey', 2001, 'ODY'),
(44, 'Deckmasters 2001', 2001, 'DKM'),
(45, 'Torment', 2002, 'TOR'),
(46, 'Judgment', 2002, 'JUD'),
(47, 'Onslaught', 2002, 'ONS'),
(48, 'Legions', 2003, 'LGN'),
(49, 'Scourge', 2003, 'SCG'),
(50, 'Eight Edition', 2003, '8ED'),
(51, 'Mirrodin', 2003, 'MRD'),
(52, 'Darksteel', 2004, 'DST'),
(53, 'Fifth Dawn', 2004, '5DN'),
(54, 'Champions of Kamigawa', 2004, 'CHK'),
(55, 'Unhinged', 2004, 'UNH'),
(56, 'Betrayers of Kamigawa', 2005, 'BOK'),
(57, 'Saviors of Kamigawa', 2005, 'SOK'),
(58, 'Ninth Edition', 2005, '9ED'),
(59, 'Salvat 2005', 2005, ''),
(60, 'Ravnica: City of Guilds', 2005, 'RAV'),
(61, 'Guildpact', 2006, 'GPT'),
(62, 'Dissension', 2006, 'DIS'),
(63, 'Coldsnap', 2006, 'CSP'),
(64, 'Time Spiral', 2006, 'TSP'),
(65, 'Planar Chaos', 2007, 'PLC'),
(66, 'Future Sight', 2007, 'FUT'),
(67, 'Tenth Edition', 2007, '10E'),
(68, 'Masters Edition', 2007, 'MED'),
(69, 'Lorwyn', 2007, 'LRW'),
(70, 'Duel Decks: Elves vs. Goblins', 2007, 'EVG'),
(71, 'Morningtide', 2008, 'MOR'),
(72, 'Shadowmoor', 2008, 'SHM'),
(73, 'Eventide', 2008, 'EVE'),
(74, 'From the Vault: Dragons', 2008, 'DRB'),
(75, 'Masters Edition II', 2008, 'ME2'),
(76, 'Shards of Alara', 2008, 'ALA'),
(77, 'Duel Decks: Jace vs. Chandra', 2008, 'DD2'),
(78, 'Conflux', 2009, 'CON'),
(79, 'Duel Decks: Divine vs. Demonic', 2009, 'DDC'),
(80, 'Alara Reborn', 2009, 'ARB'),
(81, 'Magic 2010', 2009, 'M10'),
(82, 'Commander Theme Decks', 2009, 'TD0'),
(83, 'From the Vault: Exiled', 2009, 'V09'),
(84, 'Planechase', 2009, 'HOP'),
(85, 'Masters Edition III', 2009, 'ME3'),
(86, 'Zendikar', 2009, 'ZEN'),
(87, 'Duel Decks: Garruk vs. Lilana', 2009, 'DDD'),
(88, 'Premium Deck Series: Slivers', 2009, 'H09'),
(89, 'Worldwake', 2010, 'WWK'),
(90, 'Duel Decks: Phyrexia vs. The Coalition', 2010, 'DDE'),
(91, 'Rise of the Eldrazi', 2010, 'ROE'),
(92, 'Deck Builder\'s Toolkit', 2010, ''),
(93, 'Duels of the Planeswalkers', 2010, 'DPA'),
(94, 'Archenemy', 2010, 'ARC'),
(95, 'Magic 2011', 2010, 'M11'),
(96, 'From the Vault: Relics', 2010, 'V10'),
(97, 'Duel Decks: Elspeth vs. Tezzeret', 2010, 'DDF'),
(98, 'Scars of Mirrodin', 2010, 'SOM'),
(99, 'Magic Online Deck Series', 2010, 'TD0'),
(100, 'Premium Deck Series: Fire & Lightning', 2010, 'PD2'),
(101, 'Momir Basic Event Deck', 2010, ''),
(102, 'Salvat 2011', 2011, ''),
(103, 'Master Edition IV', 2011, 'ME4'),
(104, 'Mirrodin Besieged', 2011, 'MBS'),
(105, 'Deck Builder\'s Toolkit 2011', 2011, ''),
(106, 'Duel Decks: Knights vs. Dragons', 2011, 'DDG'),
(107, 'New Phyrexia', 2011, 'NPH'),
(108, 'Commander', 2011, 'CMD'),
(109, 'Magic 2012', 2011, 'M12'),
(110, 'From the Vaults: Legends', 2011, 'V11'),
(111, 'Duel Decks: Ajani vs. Nicol Bolas', 2011, 'DDH'),
(112, 'Innistrad', 2011, 'ISD'),
(113, 'Premium Deck Series: Graveborn', 2011, 'PD3'),
(114, 'Dark Ascension', 2012, 'DKA'),
(115, 'Duel Decks: Venser vs. Koth', 2012, 'DDI'),
(116, 'Avacyn Restored', 2012, 'AVR'),
(117, 'Planechase 2012', 2012, 'PC2'),
(118, 'Magic 2013', 2012, 'M13'),
(119, 'From the Vault: Realms', 2012, 'V12'),
(120, 'Duel Decks: Izzt vs. Golgari', 2012, 'DDJ'),
(121, 'Return to Ravnica', 2012, 'RTR'),
(122, 'Commander\'s Arsenal', 2012, 'CM1'),
(123, 'Duel Decks: Mirrodin Pure vs. New Phyrexia', 2013, 'TD2'),
(124, 'Gatecrash', 2013, 'GTC'),
(125, 'Duel Decks: Sorin vs. Tibalt', 2013, 'DDK'),
(126, 'Dragon\'s Maze', 2013, 'DGM'),
(127, 'Modern Masters', 2013, 'MMA'),
(128, 'Magic 2014', 2013, 'M14'),
(129, 'From the Vault: Twenty', 2013, 'V13'),
(130, 'Duel Decks: Heros vs. Monsters', 2013, 'DDL'),
(131, 'Theros', 2013, 'THS'),
(132, 'Commander 2013', 2013, 'C13'),
(133, 'Born of the Gods', 2014, 'BNG'),
(134, 'Duel Decks: Jace vs. Vraska', 2014, 'DDM'),
(135, 'Journey into Nyx', 2014, 'JOU'),
(136, 'Modern Event Deck', 2014, 'MD1'),
(137, 'Conspiracy', 2014, 'CNS'),
(138, 'Vintage Masters', 2014, 'VMA'),
(139, 'Magic 2015', 2014, 'M15'),
(140, 'From the Vault: Annihilation', 2014, 'V14'),
(141, 'Duel Decks: Speed vs. Cunning', 2014, 'DDN'),
(142, 'Khans of Tarkir', 2014, 'KTK'),
(143, 'Commander 2014', 2014, 'C14'),
(144, 'Duel Decks Anthology', 2014, 'DD3'),
(145, 'Fate Reforged', 2015, 'FRF'),
(146, 'Duel Decks: Elspeth vs. Kiora', 2015, 'DDO'),
(147, 'Dragons of Tarkir', 2015, 'DTK'),
(148, 'Tempest Remastered', 2015, 'TPR'),
(149, 'Modern Masters 2015', 2015, 'MM2'),
(150, 'Magic Origins', 2015, 'ORI'),
(151, 'From the Vault: Angels', 2015, 'V15'),
(152, 'Duel Decks: Zendikar vs. Eldrazi', 2015, 'DDP'),
(153, 'Battle for Zendikar', 2015, 'BFZ'),
(154, 'Zendikar Expeditions', 2015, 'EXP'),
(155, 'Commander 2015', 2015, 'C15'),
(156, 'Legendary Cube', 2015, 'PZ1'),
(157, 'Oath of the Gatewatch', 2016, 'OGW'),
(158, 'Duel Decks: Blessed vs. Cursed', 2016, 'DDQ'),
(159, 'Welcome Deck 2016', 2016, 'W16'),
(160, 'Shadows over Innistrad', 2016, 'SOI'),
(161, 'Eternal Masters', 2016, 'EMA'),
(162, 'Eldritch Moon', 2016, 'EMN'),
(163, 'From the Vault: Lore', 2016, 'V16'),
(164, 'Conspiracy; Take the Crown', 2016, 'CN2'),
(165, 'Duel Decks: Nissa vs. Ob Nixilis', 2016, 'DDR'),
(166, 'Kaladesh', 2016, 'KLD'),
(167, 'Kaladesh Inventors', 2016, 'MPS'),
(168, 'Treasure Chests', 2016, 'PZ2'),
(169, 'Commander 2016', 2016, 'C16'),
(170, 'You Make the Cube', 2016, ''),
(171, 'Planechase Anthology', 2016, 'PCA'),
(172, 'Aether Revolt', 2017, 'AER'),
(173, 'Modern Masters 2017', 2017, 'MM3'),
(174, 'Duel Decks: Mind vs. Might', 2017, 'DDS'),
(175, 'Welcome Deck 2017', 2017, 'W17'),
(176, 'Amonkhet', 2017, 'AKH'),
(177, 'Amonkhet Invocations', 2017, 'MP2'),
(178, 'Commander Anthology', 2017, 'CMA'),
(179, 'Archenemy: Nicol Bolas', 2017, 'E01'),
(180, 'Hour of Devistation', 2017, 'HOU'),
(181, 'commander 2017', 2017, 'C17'),
(182, 'Ixalan', 2017, 'XLN'),
(183, 'Duel Decks: Merfolk vs. Goblins', 2017, 'DDT'),
(184, 'Iconic Masters', 2017, 'IMA'),
(185, 'Explorers of Ixalan', 2017, 'E02'),
(186, 'From the Vault: Transform', 2017, 'V17'),
(187, 'Unstable', 2017, 'UST'),
(188, 'Rivals of Ixalan', 2018, 'RIX'),
(189, 'Masters 25', 2018, 'A25'),
(190, 'Duel Decks: Elves vs. Inventors', 2018, 'DDU'),
(191, 'Challenger Decks', 2018, 'Q01'),
(192, 'Dominaria', 2018, 'DOM'),
(193, 'Commander Anthology Volume II', 2018, 'CM2'),
(194, 'Battlebond', 2018, 'BBD'),
(195, 'Signature Spellbook: Jace', 2018, 'SS1'),
(196, 'Global Series: Jiang Yanggu & Mu Yanling', 2018, 'GS1'),
(197, 'Core Set 2019', 2018, 'M19'),
(198, 'Commander 2018', 2018, 'C18'),
(199, 'Guilds of Ravnica Mythic Edition', 2018, 'MED'),
(200, 'Guilds of Ravnica', 2018, 'GRN'),
(201, 'Spellslinger Starter Kit', 2018, 'SK1'),
(202, 'Guilds of Ravnica Guild Kits', 2018, 'GK1'),
(203, 'Game Night', 2018, 'GNT'),
(204, 'Ultimate Masters', 2018, 'UMA'),
(205, 'Ravnica Allegiance Mythic Edition', 2018, 'MED'),
(206, 'Ravnica Allegiance', 2019, 'RNA'),
(207, 'Ravnica Allegiance Guild Kits', 2019, 'GK2'),
(208, 'Challenger Decks', 2019, 'Q02'),
(209, 'War of the Spark Mythic Edition', 2019, 'MED'),
(210, 'War of the Spark', 2019, 'WAR'),
(211, 'Modern Horizons', 2019, 'MH1'),
(212, 'Signature Spellbook: Gideon', 2019, 'SS2'),
(213, 'Core Set 2020', 2019, 'M20'),
(214, 'Commander 2019', 2019, 'C19'),
(215, 'Throne of Eldraine', 2019, 'ELD'),
(216, 'Mystery Booster', 2019, 'MB1'),
(217, 'Challenger Decks 2019 Japan', 2019, ''),
(218, 'Game Night 2019', 2019, 'GN2'),
(219, 'Secret Lair Drop Series', 2019, 'SLD'),
(220, 'Theros Beyond Death', 2020, 'THB'),
(221, 'Secret Lair Drop Series: Year of the Rat', 2020, 'SLD'),
(222, 'Secret Lair Drop Series: Theros Stargazing', 2020, 'SLD'),
(223, 'Unsanctioned', 2020, 'UND'),
(224, 'Secret Lair Drop Series: International Woman\'s Day', 2020, 'SLD'),
(225, 'Secret Lair Drop Series: Thalia - Beyond the Helva', 2020, 'SLD'),
(226, 'Mystery Booster Retail Edition', 2020, 'MB1'),
(227, 'Challenger Decks 2020', 2020, 'Q03'),
(228, 'Ikoria: Lair of Behemoths', 2020, 'IKO'),
(229, 'Commander 2020', 2020, 'C20'),
(230, 'Secret Lair Drop Series: The Godzilla Lands', 2020, 'SLD'),
(231, 'Secret Lair Drop Series: Summer Superdrop', 2020, 'SLD'),
(232, 'Secret Lair: Ultimate Edition', 2020, 'SS3'),
(233, 'Signature Spellbook: Chandra', 2020, 'M21'),
(234, 'Jumpstart', 2020, 'JMP'),
(235, 'Double Masters', 2020, '2XM'),
(236, 'Amonkhet Remastered', 2020, 'AKR'),
(237, 'Secret Lair Drop Series: Prime Slime', 2020, 'SLD'),
(238, 'Secret Lair Drop Series: Every Dog Has Its Day', 2020, 'SLD'),
(239, 'Zendikar Rising', 2020, 'ZNR'),
(240, 'Zendikar Rising Expeditions', 2020, 'ZNE'),
(241, 'Zendikar Rising Commander Decks', 2020, 'ZNC'),
(242, 'Secret Lair Drop Series: Extra Life 2020', 2020, 'SLD'),
(243, 'Commander Legends', 2020, 'CMR'),
(244, 'Commander Legends Commander Decks', 2020, 'CMC'),
(245, 'Secret Lair Drop Series: Secretversary', 2020, 'SLD'),
(246, 'Commander Collection: Green', 2020, 'CC1'),
(247, 'Kaldheim', 2020, ''),
(248, 'Kaldheim Commander Decks', 2020, 'KHC'),
(249, 'Secret Lair Drop Series: (February 2021)', 2020, 'SLD'),
(250, 'Time Spiral Remastered', 2021, 'TSR'),
(251, 'Secret Lair: Ultimate Edition', 2021, 'SLU'),
(252, 'Strixhaven: school of Mages', 2021, ''),
(253, 'Dungeons & Dragons: Adventures in the Forgotten Re', 2021, ''),
(254, 'Modern Horizons 2', 2021, 'MH2'),
(255, 'Innistrad: Werewolves', 2021, ''),
(256, 'Innistrad: Vampires', 2021, ''),
(257, 'Pioneer Masters', 2021, '');

-- --------------------------------------------------------

--
-- Table structure for table `CardSubType`
--

CREATE TABLE `CardSubType` (
  `ID` int(11) NOT NULL,
  `Display` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `CardSupType`
--

CREATE TABLE `CardSupType` (
  `ID` int(11) NOT NULL,
  `Display` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `CardSupType`
--

INSERT INTO `CardSupType` (`ID`, `Display`) VALUES
(1, 'Basic'),
(2, 'Elite'),
(3, 'Host'),
(4, 'Legendary'),
(5, 'Ongoing'),
(6, 'Snow'),
(7, 'Summon'),
(8, 'Token'),
(9, 'Tribal'),
(10, 'World');

-- --------------------------------------------------------

--
-- Table structure for table `CardType`
--

CREATE TABLE `CardType` (
  `ID` int(11) NOT NULL,
  `Display` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `CardType`
--

INSERT INTO `CardType` (`ID`, `Display`) VALUES
(1, 'Artifact'),
(2, 'Creature'),
(3, 'Enchantment'),
(4, 'Instant'),
(5, 'Land'),
(6, 'Planeswalker'),
(7, 'Sorcery');

-- --------------------------------------------------------

--
-- Table structure for table `Color`
--

CREATE TABLE `Color` (
  `ID` int(11) NOT NULL,
  `Black` int(11) NOT NULL,
  `Blue` int(11) NOT NULL,
  `Green` int(11) NOT NULL,
  `Red` int(11) NOT NULL,
  `White` int(11) NOT NULL,
  `Colorless` int(11) NOT NULL,
  `Display` varchar(20) NOT NULL,
  `Abv` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Color`
--

INSERT INTO `Color` (`ID`, `Black`, `Blue`, `Green`, `Red`, `White`, `Colorless`, `Display`, `Abv`) VALUES
(1, 0, 0, 0, 0, 1, 0, 'White', 'W'),
(2, 0, 0, 0, 1, 0, 0, 'Red', 'R'),
(3, 0, 0, 0, 1, 1, 0, 'Boros', 'RW'),
(4, 0, 0, 1, 0, 0, 0, 'Green', 'G'),
(5, 0, 0, 1, 0, 1, 0, 'Selesnya', 'GW'),
(6, 0, 0, 1, 1, 0, 0, 'Gruul', 'GR'),
(7, 0, 0, 1, 1, 1, 0, 'Naya', 'GRW'),
(8, 0, 1, 0, 0, 0, 0, 'Blue', 'U'),
(9, 0, 1, 0, 0, 1, 0, 'Azorius', 'UW'),
(10, 0, 1, 0, 1, 0, 0, 'Izzet', 'UR'),
(11, 0, 1, 0, 1, 1, 0, 'Jeskai', 'URW'),
(12, 0, 1, 1, 0, 0, 0, 'Simic', 'UG'),
(13, 0, 1, 1, 0, 1, 0, 'Bant', 'UGW'),
(14, 0, 1, 1, 1, 0, 0, 'Temur', 'UGR'),
(15, 0, 1, 1, 1, 1, 0, 'Non-Black', 'UGRW'),
(16, 1, 0, 0, 0, 0, 0, 'Black', 'B'),
(17, 1, 0, 0, 0, 1, 0, 'Orzhov', 'BW'),
(18, 1, 0, 0, 1, 0, 0, 'Rakdos', 'BR'),
(19, 1, 0, 0, 1, 1, 0, 'Mardu', 'BRW'),
(20, 1, 0, 1, 0, 0, 0, 'Golgari', 'BG'),
(21, 1, 0, 1, 0, 1, 0, 'Abzan', 'BGW'),
(22, 1, 0, 1, 1, 0, 0, 'Jund', 'BGR'),
(23, 1, 0, 1, 1, 1, 0, 'Non-Blue', 'BGRW'),
(24, 1, 1, 0, 0, 0, 0, 'Dimir', 'BU'),
(25, 1, 1, 0, 0, 1, 0, 'Esper', 'BUW'),
(26, 1, 1, 0, 1, 0, 0, 'Grixis', 'BUR'),
(27, 1, 1, 0, 1, 1, 0, 'Non-Green', 'BURW'),
(28, 1, 1, 1, 0, 0, 0, 'Sultai', 'BUG'),
(29, 1, 1, 1, 0, 1, 0, 'Non-Red', 'BUGW'),
(30, 1, 1, 1, 1, 0, 0, 'Non-White', 'BUGR'),
(31, 1, 1, 1, 1, 1, 0, 'Rainbow', 'BUGRW'),
(32, 0, 0, 0, 0, 0, 1, 'Colorless', 'C');

-- --------------------------------------------------------

--
-- Table structure for table `Keywords`
--

CREATE TABLE `Keywords` (
  `ID` int(11) NOT NULL,
  `Word` varchar(20) NOT NULL,
  `Description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Keywords`
--

INSERT INTO `Keywords` (`ID`, `Word`, `Description`) VALUES
(1, 'Deathtouch', 'A keyword ability that causes damage dealt by an object to a creature to be enough to destroy it.'),
(2, 'Double Strike', 'A keyword ability that lets a creature deal both first-strike and regular combat damage.'),
(3, 'Enchant', 'A keyword ability that defines what an Aura spell can target and what an Aura permanent can be attached to.'),
(4, 'Equip', 'A keyword ability that lets a player attach an Equipment to a creature they control.'),
(5, 'First Strike', 'A keyword ability that lets a creature deal its combat damage before other creatures.'),
(6, 'Flash', 'A keyword ability that lets a player play a card any time they could cast an instant.'),
(7, 'Flying', 'A keyword ability that restricts how a creature may be blocked.'),
(8, 'Haste', 'A keyword ability that lets a creature ignore the “summoning sickness” rule. '),
(9, 'Indestructible', 'A keyword ability that precludes a permanent from being destroyed.'),
(10, 'Hexproof', 'A keyword ability that precludes a permanent or player from being targeted by an opponent.'),
(11, 'Intimidate', 'A keyword ability that restricts how a creature may be blocked.'),
(12, 'Landwalk', 'A generic term for a group of keyword abilities that restrict whether a creature may be blocked.'),
(13, 'Lifelink', 'A keyword ability that causes a player to gain life.'),
(14, 'Protection', 'A keyword ability that provides a range of benefits against objects with a specific quality.'),
(15, 'Reach', 'A keyword ability that allows a creature to block an attacking creature with flying.'),
(16, 'Shroud', 'A keyword ability that precludes a permanent or player from being targeted. '),
(17, 'Trample', 'A keyword ability that modifies how a creature assigns combat damage.'),
(18, 'Vigilance', 'A keyword ability that lets a creature attack without tapping.'),
(19, 'Banding', 'A keyword ability that modifies the rules for declaring attackers and assigning combat damage. “Bands with other” is a specialized version of the ability.'),
(20, 'Rampage', 'A keyword ability that can make a creature better in combat.'),
(21, 'Cumulative Upkeep', 'A keyword ability that imposes an increasing cost to keep a permanent on the battlefield.'),
(22, 'Flanking', 'A keyword ability that can make a creature better in combat.'),
(23, 'Phasing', 'A keyword ability that causes a permanent to sometimes be treated as though it does not exist.'),
(24, 'Buyback', 'A keyword ability of instants and sorceries that can let the spell return to its owner’s hand as it resolves.'),
(25, 'Shadow', 'A keyword ability that restricts how a creature may be blocked and which creatures it can block.'),
(26, 'Cycling', 'A keyword ability that lets a card be discarded and replaced with a new card.'),
(27, 'Echo', 'A keyword ability that imposes a cost to keep a permanent on the battlefield. '),
(28, 'Horsemanship', 'A keyword ability that restricts how a creature may be blocked.'),
(29, 'Fading', 'A keyword ability that limits how long a permanent remains on the battlefield.'),
(30, 'Kicker', 'Kicker is a keyword ability that represents an optional additional cost. A spell has been kicked if its controller declared the intention to pay any or all of its kicker costs.'),
(31, 'Flashback', 'A keyword ability that lets a player cast a card from their graveyard.'),
(32, 'Madness', 'A keyword ability that lets a player cast a card they discard.'),
(33, 'Fear', 'A keyword ability that restricts how a creature may be blocked.'),
(34, 'Morph', 'A keyword ability that lets a card be cast face down as a 2/2 creature.'),
(35, 'Amplify', 'A keyword ability than can have a creature enter the battlefield with +1/+1 counters on it.'),
(36, 'Provoke', 'A keyword ability that can force a creature to block.'),
(37, 'Storm', 'A keyword ability that creates copies of a spell.'),
(38, 'Affinity', 'A keyword ability that reduces how much mana you need to spend to cast a spell.'),
(39, 'Entwine', 'A keyword ability that lets a player choose all modes for a spell rather than just the number specified.'),
(40, 'Sunburst', 'A keyword ability that can have a permanent enter the battlefield with +1/+1 counters or charge counters on it.'),
(41, 'Modular', 'A keyword ability that has a permanent enter the battlefield with +1/+1 counters on it and can move those counters to other artifact creatures.'),
(42, 'Soulshift', 'A keyword ability that lets a player return a card from their graveyard to their hand.'),
(43, 'Bushido', 'A keyword ability that can make a creature better in combat.'),
(44, 'Splice', 'A keyword ability that lets a player add a card’s rules text onto another spell. '),
(45, 'Offering', 'A keyword ability that modifies when you can cast a spell and how much mana you need to spend to do it.'),
(46, 'Ninjutsu', 'A keyword ability that lets a creature suddenly enter combat.'),
(47, 'Epic', 'A keyword ability that lets a player copy a spell at the beginning of each of their upkeeps at the expense of casting any other spells for the rest of the game.'),
(48, 'Convoke', 'A keyword ability that lets you tap creatures rather than pay mana to cast a spell.'),
(49, 'Dredge', 'A keyword ability that lets a player return a card from their graveyard to their hand.'),
(50, 'Transmute', 'A keyword ability that lets a player search their library for a replacement card.'),
(51, 'Defender', 'A keyword ability that prohibits a creature from attacking.'),
(52, 'Double Strike', 'A keyword ability that lets a creature deal both first-strike and regular combat damage.'),
(53, 'Enchant', 'A keyword ability that defines what an Aura spell can target and what an Aura permanent can be attached to.'),
(54, 'Equip', 'A keyword ability that lets a player attach an Equipment to a creature they control.'),
(55, 'First Strike', 'A keyword ability that lets a creature deal its combat damage before other creatures.'),
(56, 'Flash', 'A keyword ability that lets a player play a card any time they could cast an instant.'),
(57, 'Flying', 'A keyword ability that restricts how a creature may be blocked.'),
(58, 'Haste', 'A keyword ability that lets a creature ignore the “summoning sickness” rule. '),
(59, 'Indestructible', 'A keyword ability that precludes a permanent from being destroyed.'),
(60, 'Hexproof', 'A keyword ability that precludes a permanent or player from being targeted by an opponent.'),
(61, 'Intimidate', 'A keyword ability that restricts how a creature may be blocked.'),
(62, 'Landwalk', 'A generic term for a group of keyword abilities that restrict whether a creature may be blocked.'),
(63, 'Lifelink', 'A keyword ability that causes a player to gain life.'),
(64, 'Protection', 'A keyword ability that provides a range of benefits against objects with a specific quality.'),
(65, 'Reach', 'A keyword ability that allows a creature to block an attacking creature with flying.'),
(66, 'Shroud', 'A keyword ability that precludes a permanent or player from being targeted. '),
(67, 'Trample', 'A keyword ability that modifies how a creature assigns combat damage.'),
(68, 'Vigilance', 'A keyword ability that lets a creature attack without tapping.'),
(69, 'Banding', 'A keyword ability that modifies the rules for declaring attackers and assigning combat damage. “Bands with other” is a specialized version of the ability.'),
(70, 'Rampage', 'A keyword ability that can make a creature better in combat.'),
(71, 'Cumulative Upkeep', 'A keyword ability that imposes an increasing cost to keep a permanent on the battlefield.'),
(72, 'Flanking', 'A keyword ability that can make a creature better in combat.'),
(73, 'Phasing', 'A keyword ability that causes a permanent to sometimes be treated as though it does not exist.'),
(74, 'Buyback', 'A keyword ability of instants and sorceries that can let the spell return to its owner’s hand as it resolves.'),
(75, 'Shadow', 'A keyword ability that restricts how a creature may be blocked and which creatures it can block.'),
(76, 'Cycling', 'A keyword ability that lets a card be discarded and replaced with a new card.'),
(77, 'Echo', 'A keyword ability that imposes a cost to keep a permanent on the battlefield. '),
(78, 'Horsemanship', 'A keyword ability that restricts how a creature may be blocked.'),
(79, 'Fading', 'A keyword ability that limits how long a permanent remains on the battlefield.'),
(80, 'Kicker', 'Kicker is a keyword ability that represents an optional additional cost. A spell has been kicked if its controller declared the intention to pay any or all of its kicker costs.'),
(81, 'Flashback', 'A keyword ability that lets a player cast a card from their graveyard.'),
(82, 'Madness', 'A keyword ability that lets a player cast a card they discard.'),
(83, 'Fear', 'A keyword ability that restricts how a creature may be blocked.'),
(84, 'Morph', 'A keyword ability that lets a card be cast face down as a 2/2 creature.'),
(85, 'Amplify', 'A keyword ability than can have a creature enter the battlefield with +1/+1 counters on it.'),
(86, 'Provoke', 'A keyword ability that can force a creature to block.'),
(87, 'Storm', 'A keyword ability that creates copies of a spell.'),
(88, 'Affinity', 'A keyword ability that reduces how much mana you need to spend to cast a spell.'),
(89, 'Entwine', 'A keyword ability that lets a player choose all modes for a spell rather than just the number specified.'),
(90, 'Sunburst', 'A keyword ability that can have a permanent enter the battlefield with +1/+1 counters or charge counters on it.'),
(91, 'Modular', 'A keyword ability that has a permanent enter the battlefield with +1/+1 counters on it and can move those counters to other artifact creatures.'),
(92, 'Soulshift', 'A keyword ability that lets a player return a card from their graveyard to their hand.'),
(93, 'Bushido', 'A keyword ability that can make a creature better in combat.'),
(94, 'Splice', 'A keyword ability that lets a player add a card’s rules text onto another spell. '),
(95, 'Offering', 'A keyword ability that modifies when you can cast a spell and how much mana you need to spend to do it.'),
(96, 'Ninjutsu', 'A keyword ability that lets a creature suddenly enter combat.'),
(97, 'Epic', 'A keyword ability that lets a player copy a spell at the beginning of each of their upkeeps at the expense of casting any other spells for the rest of the game.'),
(98, 'Convoke', 'A keyword ability that lets you tap creatures rather than pay mana to cast a spell.'),
(99, 'Dredge', 'A keyword ability that lets a player return a card from their graveyard to their hand.'),
(100, 'Transmute', 'A keyword ability that lets a player search their library for a replacement card.'),
(101, 'Bloodthirst', 'A keyword ability that can have a creature enter the battlefield with +1/+1 counters on it.'),
(102, 'Haunt', 'A keyword ability that exiles cards. A card exiled this way “haunts” a creature targeted by the haunt ability.'),
(103, 'Replicate', 'A keyword ability that creates copies of a spell.'),
(104, 'Forecast', 'A keyword ability that allows an activated ability to be activated from a player’s hand.'),
(105, 'Graft', 'A keyword ability that has a permanent enter the battlefield with +1/+1 counters on it and can move those counters to other creatures.'),
(106, 'Recover', 'A keyword ability that lets a player return a card from their graveyard to their hand.'),
(107, 'Ripple', 'A keyword ability that may let a player cast extra cards from their library for no cost.'),
(108, 'Split Second', 'A keyword ability that makes it nearly impossible for a player to respond to a spell.'),
(109, 'Suspend', 'A keyword ability that provides an alternative way to play a card.'),
(110, 'Vanishing', 'A keyword ability that limits how long a permanent remains on the battlefield.'),
(111, 'Absorb', 'A keyword ability that prevents damage.'),
(112, 'Aura Swap', 'A keyword ability that lets you exchange an Aura on the battlefield with one in your hand.'),
(113, 'Delve', 'A keyword ability that lets you exile cards from your graveyard rather than pay generic mana to cast a spell.'),
(114, 'Fortify', 'A keyword ability that lets a player attach a Fortification to a land they control.'),
(115, 'Frenzy', 'A keyword ability that can make a creature better in combat.'),
(116, 'Gravestorm', 'A keyword ability that creates copies of a spell.'),
(117, 'Poisonous', 'A keyword ability that causes a player to get poison counters.'),
(118, 'Transfigure', 'A keyword ability that lets a player search their library for a replacement creature card.'),
(119, 'Champion', 'A keyword ability that lets one creature temporarily replace another. A permanent is “championed” by another permanent if the latter exiles the former as the direct result of a champion ability.'),
(120, 'Changeling', 'A characteristic-defining ability that grants the object it’s on every creature type.'),
(121, 'Evoke', 'A keyword ability that causes a permanent to be sacrificed when it enters the battlefield.'),
(122, 'Hideaway', 'A keyword ability that lets a player store a secret card.'),
(123, 'Prowl', 'A keyword ability that may allow a spell to be cast for an alternative cost. '),
(124, 'Reinforce', 'A keyword ability that lets a player put +1/+1 counters on a creature. '),
(125, 'Conspire', 'A keyword ability that creates a copy of a spell. '),
(126, 'Persist', 'A keyword ability that can return a creature from the graveyard to the battlefield.'),
(127, 'Wither', 'A keyword ability that affects how an object deals damage to a creature. '),
(128, 'Retrace', 'A keyword ability that lets a player cast a card from their graveyard.'),
(129, 'Devour', 'A keyword ability that can have a creature enter the battlefield with +1/+1 counters on it.'),
(130, 'Exalted', 'A keyword ability that can make a creature better in combat.'),
(131, 'Unearth', 'A keyword ability that lets a player return a creature card from their graveyard to the battlefield.'),
(132, 'Cascade', 'A keyword ability that may let a player cast a random extra spell for no cost. '),
(133, 'Annihilator', 'A keyword ability that can make a creature particularly brutal when it attacks.'),
(134, 'Level Up', 'A keyword ability that can put level counters on a creature.'),
(135, 'Rebound', 'A keyword ability that allows an instant or sorcery spell to be cast a second time.'),
(136, 'Totem Armor', 'A keyword ability that allows an Aura to protect the permanent it’s enchanting.'),
(137, 'Infect', 'A keyword ability that affects how an object deals damage to creatures and players.'),
(138, 'Battle Cry', 'A keyword ability that makes other attacking creatures better in combat.'),
(139, 'Living Weapon', 'A keyword ability that creates a creature token and then attaches the Equipment with the ability to that token.'),
(140, 'Undying', 'A keyword ability that can return a creature from the graveyard to the battlefield.'),
(141, 'Miracle', 'A keyword ability that lets you cast a spell for a reduced cost if it’s the first card you draw in a turn.'),
(142, 'Soulbond', 'A keyword ability that makes creatures better by pairing them together.'),
(143, 'Overload', 'A keyword ability that allows a spell to affect either a single target or many objects.'),
(144, 'Scavenge', 'A keyword ability that allows you to exile a creature card from your graveyard to put +1/+1 counters on a creature.'),
(145, 'Unleash', 'A keyword ability that allows a creature to enter the battlefield with a +1/+1 counter on it and stops it from blocking if it has a +1/+1 counter on it.'),
(146, 'Cipher', 'A keyword ability that allows you to encode a card on a creature and cast that card whenever that creature deals combat damage to a player.'),
(147, 'Evolve', 'A keyword ability that lets you put a +1/+1 counter on a creature when a larger creature enters the battlefield under your control.'),
(148, 'Extort', 'A keyword ability that lets you gain life and have opponents lose life whenever you cast a spell.'),
(149, 'Fuse', 'A keyword ability that allows a player to cast both halves of a split card. '),
(150, 'Bestow', 'A keyword ability that lets a creature card be cast as an Aura.'),
(151, 'Tribute', 'A keyword ability that allows an opponent to choose between a creature entering the battlefield with +1/+1 counters or an additional ability.'),
(152, 'Dethrone', 'A keyword ability that puts a +1/+1 counter on a creature when it attacks the player with the most life.'),
(153, 'Hidden Agenda', 'A keyword ability that allows a conspiracy card to be put into the command zone face down.'),
(154, 'Outlast', 'A keyword ability that allows a creature to grow larger over time.'),
(155, 'Prowess', 'A keyword ability that causes a creature to get +1/+1 whenever its controller casts a noncreature spell.'),
(156, 'Dash', 'A keyword ability that allows creatures to be especially aggressive.'),
(157, 'Exploit', 'A keyword ability that lets you sacrifice a creature for a benefit.'),
(158, 'Menace', 'An evasion ability that makes creatures unblockable by a single creature. '),
(159, 'Renown', 'A keyword ability that makes a creature stronger after it deals combat damage to a player.'),
(160, 'Awaken', 'A keyword ability that lets you turn a land you control into a creature.'),
(161, 'Devoid', 'A characteristic-defining ability that makes an object colorless.'),
(162, 'Ingest', 'A keyword ability that can exile the top card of a player’s library.'),
(163, 'Myriad', 'A triggered ability that effectively lets a creature attack in all possible directions.'),
(164, 'Surge', 'A keyword ability that provides an alternative cost to cast a card if you or one of your teammates has cast another spell in the same turn.'),
(165, 'Skulk', 'A keyword ability that restricts how a creature may be blocked.'),
(166, 'Emerge', 'A keyword ability that lets a player cast a spell for less by sacrificing a creature.'),
(167, 'Escalate', 'A keyword ability on some modal spells that adds a cost for choosing additional modes.'),
(168, 'Melee', 'A keyword ability that improves an attacking creature based on the number of opponents you attacked.'),
(169, 'Crew', 'A keyword ability that lets you tap creatures to turn a Vehicle into an artifact creature.'),
(170, 'Partner', 'A keyword ability that lets two legendary creatures or planeswalkers be your commander in the Commander variant rather than one. “Partner with [name]” is a specialized version of the ability that works even outside of the Commander variant to help two cards reach the battlefield together.'),
(171, 'Undaunted', 'A keyword ability that reduces the cost of a spell based on the number of opponents you have.'),
(172, 'Improvise', 'A keyword ability that lets you tap artifacts rather than pay mana to cast a spell.'),
(173, 'Aftermath', 'A keyword ability that lets a player cast one half of a split card only from their graveyard.'),
(174, 'Embalm', 'A keyword ability that lets a player exile a creature card from their graveyard to create a mummified token version of that card.'),
(175, 'Eternalize', 'A keyword ability that lets a player exile a creature card from their graveyard to create an eternalized token version of that card.'),
(176, 'Afflict', 'A keyword ability that makes the defending player lose life for blocking.'),
(177, 'Ascend', 'A keyword causing a player to get the designation of the city’s blessing once they control ten permanents.'),
(178, 'Assist', 'A keyword ability that lets another player help you pay for a spell.'),
(179, 'Jump-Start', 'A keyword ability that lets a player cast a card from their graveyard by discarding a card.'),
(180, 'Mentor', 'A keyword ability that lets your bigger creatures power up your smaller creatures when they attack together.'),
(181, 'Afterlife', 'A keyword ability that leaves behind Spirit creature tokens when certain creatures die.'),
(182, 'Riot', 'A keyword ability that lets a player choose whether certain creatures enter the battlefield with haste or with a +1/+1 counter.'),
(183, 'Spectacle', 'A keyword ability that allows certain spells to be cast for an alternative cost if an opponent has lost life.'),
(184, 'Escape', 'A keyword ability that lets a player cast a card from their graveyard.'),
(185, 'Companion', 'A keyword ability that allows a player to choose one creature card from outside the game as a companion if the restriction of that card’s companion ability is met. Once a player has chosen a companion, that player may pay 3<Open> to put it into their hand once during the game.'),
(186, 'Mutate', 'A keyword that lets a creature card be cast as a mutating creature spell.'),
(187, 'Encore', 'A keyword ability that lets a player exile a creature card from their graveyard to, for each opponent, create a token that’s a copy of that card to attack that opponent.'),
(188, 'Fabricate', 'A keyword ability that lets you choose whether to create Servo tokens or put +1/+1 counters on a creature.');

-- --------------------------------------------------------

--
-- Table structure for table `RelatCardKeyword`
--

CREATE TABLE `RelatCardKeyword` (
  `CardID` int(11) NOT NULL,
  `KeywordID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `RelatCardSubType`
--

CREATE TABLE `RelatCardSubType` (
  `CardID` int(11) NOT NULL,
  `SubTypeID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `RelatCardSupType`
--

CREATE TABLE `RelatCardSupType` (
  `CardID` int(11) NOT NULL,
  `SupTypeID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `RelatCardType`
--

CREATE TABLE `RelatCardType` (
  `CardID` int(11) NOT NULL,
  `TypeID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Artists`
--
ALTER TABLE `Artists`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `Card`
--
ALTER TABLE `Card`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `SetID` (`SetID`),
  ADD KEY `ArtistID` (`ArtistID`),
  ADD KEY `ColorID` (`ColorID`);

--
-- Indexes for table `CardSet`
--
ALTER TABLE `CardSet`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `CardSubType`
--
ALTER TABLE `CardSubType`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `CardSupType`
--
ALTER TABLE `CardSupType`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `CardType`
--
ALTER TABLE `CardType`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `Color`
--
ALTER TABLE `Color`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `Keywords`
--
ALTER TABLE `Keywords`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `RelatCardKeyword`
--
ALTER TABLE `RelatCardKeyword`
  ADD PRIMARY KEY (`CardID`,`KeywordID`),
  ADD KEY `KeywordID` (`KeywordID`);

--
-- Indexes for table `RelatCardSubType`
--
ALTER TABLE `RelatCardSubType`
  ADD PRIMARY KEY (`CardID`,`SubTypeID`),
  ADD KEY `SubTypeID` (`SubTypeID`);

--
-- Indexes for table `RelatCardSupType`
--
ALTER TABLE `RelatCardSupType`
  ADD PRIMARY KEY (`CardID`,`SupTypeID`),
  ADD KEY `SupTypeID` (`SupTypeID`);

--
-- Indexes for table `RelatCardType`
--
ALTER TABLE `RelatCardType`
  ADD PRIMARY KEY (`CardID`,`TypeID`),
  ADD KEY `TypeID` (`TypeID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Artists`
--
ALTER TABLE `Artists`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=582;

--
-- AUTO_INCREMENT for table `Card`
--
ALTER TABLE `Card`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `CardSet`
--
ALTER TABLE `CardSet`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=258;

--
-- AUTO_INCREMENT for table `CardSubType`
--
ALTER TABLE `CardSubType`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `CardSupType`
--
ALTER TABLE `CardSupType`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `CardType`
--
ALTER TABLE `CardType`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `Keywords`
--
ALTER TABLE `Keywords`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=189;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Card`
--
ALTER TABLE `Card`
  ADD CONSTRAINT `Card_ibfk_1` FOREIGN KEY (`SetID`) REFERENCES `CardSet` (`ID`),
  ADD CONSTRAINT `Card_ibfk_2` FOREIGN KEY (`ArtistID`) REFERENCES `Artists` (`ID`),
  ADD CONSTRAINT `Card_ibfk_3` FOREIGN KEY (`ColorID`) REFERENCES `Color` (`ID`);

--
-- Constraints for table `RelatCardKeyword`
--
ALTER TABLE `RelatCardKeyword`
  ADD CONSTRAINT `RelatCardKeyword_ibfk_1` FOREIGN KEY (`CardID`) REFERENCES `Card` (`ID`),
  ADD CONSTRAINT `RelatCardKeyword_ibfk_2` FOREIGN KEY (`KeywordID`) REFERENCES `Keywords` (`ID`);

--
-- Constraints for table `RelatCardSubType`
--
ALTER TABLE `RelatCardSubType`
  ADD CONSTRAINT `RelatCardSubType_ibfk_1` FOREIGN KEY (`CardID`) REFERENCES `Card` (`ID`),
  ADD CONSTRAINT `RelatCardSubType_ibfk_2` FOREIGN KEY (`SubTypeID`) REFERENCES `CardSubType` (`ID`);

--
-- Constraints for table `RelatCardSupType`
--
ALTER TABLE `RelatCardSupType`
  ADD CONSTRAINT `RelatCardSupType_ibfk_1` FOREIGN KEY (`CardID`) REFERENCES `Card` (`ID`),
  ADD CONSTRAINT `RelatCardSupType_ibfk_2` FOREIGN KEY (`SupTypeID`) REFERENCES `CardSupType` (`ID`);

--
-- Constraints for table `RelatCardType`
--
ALTER TABLE `RelatCardType`
  ADD CONSTRAINT `RelatCardType_ibfk_1` FOREIGN KEY (`CardID`) REFERENCES `Card` (`ID`),
  ADD CONSTRAINT `RelatCardType_ibfk_2` FOREIGN KEY (`TypeID`) REFERENCES `CardType` (`ID`);
--
-- Database: `maindb`
--
CREATE DATABASE IF NOT EXISTS `maindb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `maindb`;

-- --------------------------------------------------------

--
-- Table structure for table `Collections`
--

CREATE TABLE `Collections` (
  `ID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Decks`
--

CREATE TABLE `Decks` (
  `ID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `DeckStats`
--

CREATE TABLE `DeckStats` (
  `DeckID` int(11) NOT NULL,
  `Wins` int(11) NOT NULL,
  `Losses` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `RelatCardCollection`
--

CREATE TABLE `RelatCardCollection` (
  `CardID` int(11) NOT NULL,
  `CollectionID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `RelatCardDeck`
--

CREATE TABLE `RelatCardDeck` (
  `CardID` int(11) NOT NULL,
  `DeckID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `UserStats`
--

CREATE TABLE `UserStats` (
  `UserID` int(11) NOT NULL,
  `Wins` int(11) NOT NULL,
  `Losses` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Collections`
--
ALTER TABLE `Collections`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `UserID` (`UserID`);

--
-- Indexes for table `Decks`
--
ALTER TABLE `Decks`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `UserID` (`UserID`);

--
-- Indexes for table `DeckStats`
--
ALTER TABLE `DeckStats`
  ADD PRIMARY KEY (`DeckID`);

--
-- Indexes for table `RelatCardCollection`
--
ALTER TABLE `RelatCardCollection`
  ADD PRIMARY KEY (`CardID`,`CollectionID`),
  ADD KEY `CollectionID` (`CollectionID`);

--
-- Indexes for table `RelatCardDeck`
--
ALTER TABLE `RelatCardDeck`
  ADD PRIMARY KEY (`CardID`,`DeckID`),
  ADD KEY `DeckID` (`DeckID`);

--
-- Indexes for table `UserStats`
--
ALTER TABLE `UserStats`
  ADD PRIMARY KEY (`UserID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Collections`
--
ALTER TABLE `Collections`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Decks`
--
ALTER TABLE `Decks`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Collections`
--
ALTER TABLE `Collections`
  ADD CONSTRAINT `Collections_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `userdb`.`Users` (`ID`);

--
-- Constraints for table `Decks`
--
ALTER TABLE `Decks`
  ADD CONSTRAINT `Decks_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `userdb`.`Users` (`ID`);

--
-- Constraints for table `DeckStats`
--
ALTER TABLE `DeckStats`
  ADD CONSTRAINT `DeckStats_ibfk_1` FOREIGN KEY (`DeckID`) REFERENCES `Decks` (`ID`);

--
-- Constraints for table `RelatCardCollection`
--
ALTER TABLE `RelatCardCollection`
  ADD CONSTRAINT `RelatCardCollection_ibfk_1` FOREIGN KEY (`CardID`) REFERENCES `carddb`.`Card` (`ID`),
  ADD CONSTRAINT `RelatCardCollection_ibfk_2` FOREIGN KEY (`CollectionID`) REFERENCES `Collections` (`ID`);

--
-- Constraints for table `RelatCardDeck`
--
ALTER TABLE `RelatCardDeck`
  ADD CONSTRAINT `RelatCardDeck_ibfk_1` FOREIGN KEY (`CardID`) REFERENCES `carddb`.`Card` (`ID`),
  ADD CONSTRAINT `RelatCardDeck_ibfk_2` FOREIGN KEY (`DeckID`) REFERENCES `Decks` (`ID`);

--
-- Constraints for table `UserStats`
--
ALTER TABLE `UserStats`
  ADD CONSTRAINT `UserStats_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `userdb`.`Users` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
