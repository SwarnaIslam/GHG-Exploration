import {
  facebook,
  instagram,
  shieldTick,
  support,
  truckFast,
  twitter,
} from "../icons";
import {
  p1,
  p2,
  p3,
  p4,
  p5,
  a1,
  a2,
  a3,
  a4,
  a5,
  d1,
  d2,
  d3,
  d4,
  d5,
} from "../images";
import { h1, h2, h3, h4 } from "../images";
export const navLinks = [
  { href: "/", label: "Home" },
  { href: "/notif", label: "Get Notification" },
  { href: "/login", label: "Login" },
];

export const rand_pics = [
  {
    imgURL: p1,
    label: "Talk to Ogrobot",
    href: "/ogrobot",
  },
  {
    imgURL: p2,
    label: "Games",
    href: "/game",
  },
  {
    imgURL: p3,
    label: "Learn about Green House Gases",
    href: "/education",
  },
  {
    imgURL: p4,
    label: "Quiz",
    href: "/login",
  },
  {
    imgURL: p5,
    label: "Explore GHG Map",
    href: "/map",
  },
];

export const hero_pics = [
  {
    imgURL: h4,
    label: "Login for notifications",
    href: "/notif",
  }
];

export const src = [
  { id: "household", imgURL: a1, category: "human" },
  { id: "decomposition", imgURL: d1, category: "natural" },
  { id: "oceanic", imgURL: d2, category: "natural" },
  { id: "electricity", imgURL: a2, category: "human" },
  { id: "wildfire", imgURL: d3, category: "natural" },
  { id: "agriculture", imgURL: a3, category: "human" },
  { id: "manufacturing", imgURL: a4, category: "human" },
  { id: "volcano", imgURL: d4, category: "natural" },
  { id: "transport", imgURL: a5, category: "human" },
  { id: "respiration", imgURL: d5, category: "natural" },
];

export const src_drop = [
  { id: "human", imgURL: a1 },
  { id: "dog", imgURL: a2 },
];

export const statistics = [
  { value: "80.82 g ", label: "Average Emission ", unit: "(CO2/m²/yr)" },
  { value: "27670.27 g ", label: "Max Emission ", unit: "(CO2/m²/yr)" },
];

export const footerLinks = [
  {
    title: "Education",
    links: [
      { name: "Games", link: "/" },
      { name: "Quizzes", link: "/" },
      { name: "Awareness", link: "/" },
      { name: "View Map", link: "/" },
      { name: "Get Notifications", link: "/" },
    ],
  },
  {
    title: "Help",
    links: [
      { name: "About us", link: "/" },
      { name: "FAQs", link: "/" },
      { name: "How it works", link: "/" },
      { name: "Privacy policy", link: "/" },
    ],
  },
  {
    title: "Get in touch",
    links: [
      {
        name: "customer@ghg_explorer.com",
        link: "mailto:customer@ghg_explorer.com",
      },
      { name: "+92554862354", link: "tel:+92554862354" },
    ],
  },
];

export const socialMedia = [
  { src: facebook, alt: "facebook logo" },
  { src: twitter, alt: "twitter logo" },
  { src: instagram, alt: "instagram logo" },
];
